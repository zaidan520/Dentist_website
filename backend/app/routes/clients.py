# # backend/app/routes/clients.py
# from fastapi import APIRouter, Depends, HTTPException, Request
# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy import select
# import os
# from ..database import get_db
# from ..models import Client
# from ..schemas import ClientCreate, ClientResponse
# from ..utils.slug import make_slug

# router = APIRouter(prefix="/api/clients", tags=["clients"])

# @router.post("/register", response_model=dict)
# async def register_client(
#     request: Request,
#     data: ClientCreate,
#     db: AsyncSession = Depends(get_db)
# ):
#     # Validate required
#     if not data.business_name or not data.business_name.strip():
#         raise HTTPException(status_code=400, detail="business_name is required")

#     slug = make_slug(data.business_name.strip())

#     # Build demo URL
#     base_url = os.getenv("DEMO_BASE_URL", "http://localhost:4321")
#     demo_url = f"{base_url}/{slug}"

#     # Check if client already exists
#     stmt = select(Client).where(Client.slug == slug)
#     result = await db.execute(stmt)
#     existing = result.scalar_one_or_none()

#     if existing:
#         # Update
#         for key, value in data.dict(exclude_unset=True).items():
#             setattr(existing, key, value)
#         existing.demo_url = demo_url
#         existing.updated_at = datetime.utcnow()
#     else:
#         # Create new
#         new_client = Client(
#             slug=slug,
#             business_name=data.business_name.strip(),
#             niche=data.niche,
#             phone=data.phone,
#             address=data.address,
#             email=data.email,
#             city=data.city,
#             state=data.state,
#             rating=data.rating,
#             google_maps_url=data.google_maps_url,
#             facebook_url=data.facebook_url,
#             instagram_url=data.instagram_url,
#             lead_score=data.lead_score,
#             demo_url=demo_url,
#         )
#         db.add(new_client)

#     await db.commit()

#     return {
#         "success": True,
#         "slug": slug,
#         "demo_url": demo_url,
#         "message": f"Demo page ready at {demo_url}"
#     }

# @router.get("/{slug}", response_model=ClientResponse)
# async def get_client(slug: str, db: AsyncSession = Depends(get_db)):
#     stmt = select(Client).where(Client.slug == slug)
#     result = await db.execute(stmt)
#     client = result.scalar_one_or_none()
#     if not client:
#         raise HTTPException(status_code=404, detail="Client not found")
#     return client


# backend/app/routes/clients.py
from datetime import datetime, date
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Request, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import os
from ..database import get_db
from ..models import Client
from ..schemas import ClientCreate, ClientResponse
from ..utils.slug import make_slug

router = APIRouter(prefix="/api/clients", tags=["clients"])


@router.post("/register", response_model=dict)
async def register_client(
    request: Request,
    data: ClientCreate,
    db: AsyncSession = Depends(get_db)
):
    # Validate required
    if not data.business_name or not data.business_name.strip():
        raise HTTPException(status_code=400, detail="business_name is required")

    slug = make_slug(data.business_name.strip())

    # Build demo URL
    base_url = os.getenv("DEMO_BASE_URL", "http://localhost:4321")
    demo_url = f"{base_url}/{slug}"

    # Check if client already exists
    stmt = select(Client).where(Client.slug == slug)
    result = await db.execute(stmt)
    existing = result.scalar_one_or_none()

    if existing:
        # Update
        for key, value in data.dict(exclude_unset=True).items():
            setattr(existing, key, value)
        existing.demo_url = demo_url
        existing.updated_at = datetime.utcnow()
    else:
        # Create new
        new_client = Client(
            slug=slug,
            business_name=data.business_name.strip(),
            niche=data.niche,
            phone=data.phone,
            address=data.address,
            email=data.email,
            city=data.city,
            state=data.state,
            rating=data.rating,
            google_maps_url=data.google_maps_url,
            facebook_url=data.facebook_url,
            instagram_url=data.instagram_url,
            lead_score=data.lead_score,
            latitude=data.latitude,
            longitude=data.longitude,
            demo_url=demo_url,
        )
        db.add(new_client)

    await db.commit()

    return {
        "success": True,
        "slug": slug,
        "demo_url": demo_url,
        "message": f"Demo page ready at {demo_url}"
    }


# IMPORTANT: this route must be declared BEFORE the "/{slug}" route below.
# FastAPI matches routes top-to-bottom, and "/{slug}" would otherwise swallow
# the literal path "/demo-links" by treating "demo-links" as a slug value.
@router.get("/demo-links", response_model=dict)
async def get_demo_links(
    since: Optional[date] = Query(
        None,
        description="Only include clients created/updated on or after this date (YYYY-MM-DD).",
    ),
    db: AsyncSession = Depends(get_db),
):
    """
    Returns a flat mapping of slug -> demo_url for every registered client.
    Used by Agent3 to fetch live demo links without touching the filesystem
    or the database directly.

    Optional ?since=YYYY-MM-DD filters to clients created OR updated on/after
    that date, so Agent3 can ask for "just today's new clients" instead of
    pulling the entire list every run.
    """
    stmt = select(Client.slug, Client.demo_url, Client.created_at, Client.updated_at)

    if since is not None:
        # Combine the date with midnight so we compare against full datetimes
        since_dt = datetime.combine(since, datetime.min.time())
        stmt = stmt.where(
            (Client.created_at >= since_dt) | (Client.updated_at >= since_dt)
        )

    result = await db.execute(stmt)
    rows = result.all()

    links = {
        row.slug: row.demo_url
        for row in rows
        if row.demo_url is not None
    }

    return {
        "success": True,
        "count": len(links),
        "since": since.isoformat() if since else None,
        "links": links,
    }


@router.get("/{slug}", response_model=ClientResponse)
async def get_client(slug: str, db: AsyncSession = Depends(get_db)):
    stmt = select(Client).where(Client.slug == slug)
    result = await db.execute(stmt)
    client = result.scalar_one_or_none()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client