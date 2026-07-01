# # backend/app/models.py
# from sqlalchemy import Column, Integer, String, DateTime, Text
# from .database import Base
# import datetime

# class Client(Base):
#     __tablename__ = "clients"

#     id = Column(Integer, primary_key=True, index=True)
#     slug = Column(String, unique=True, index=True, nullable=False)
#     business_name = Column(String, nullable=False)
#     niche = Column(String, nullable=False, default="restaurant")
#     phone = Column(String, nullable=True)
#     address = Column(String, nullable=True)
#     email = Column(String, nullable=True)
#     city = Column(String, nullable=True)
#     state = Column(String, nullable=True)
#     rating = Column(String, nullable=True)          # e.g., "4.6"
#     google_maps_url = Column(String, nullable=True)
#     facebook_url = Column(String, nullable=True)
#     instagram_url = Column(String, nullable=True)
#     lead_score = Column(String, nullable=True)
#     demo_url = Column(String, nullable=True)        # built from base + slug
#     created_at = Column(DateTime, default=datetime.datetime.utcnow)
#     updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

#     # Additional fields you may want:
#     # latitude, longitude, etc. Add as needed.

# backend/app/models.py
from sqlalchemy import Column, Integer, String, DateTime, Text
from .database import Base
import datetime

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String, unique=True, index=True, nullable=False)
    business_name = Column(String, nullable=False)
    niche = Column(String, nullable=False, default="restaurant")
    phone = Column(String, nullable=True)
    address = Column(String, nullable=True)
    email = Column(String, nullable=True)
    city = Column(String, nullable=True)
    state = Column(String, nullable=True)
    rating = Column(String, nullable=True)          # e.g., "4.6"
    google_maps_url = Column(String, nullable=True)
    facebook_url = Column(String, nullable=True)
    instagram_url = Column(String, nullable=True)
    lead_score = Column(String, nullable=True)
    latitude = Column(String, nullable=True)
    longitude = Column(String, nullable=True)
    demo_url = Column(String, nullable=True)        # built from base + slug
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    # Additional fields you may want:
    # latitude, longitude, etc. Add as needed.