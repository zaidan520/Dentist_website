# # backend/app/schemas.py
# from pydantic import BaseModel, EmailStr, Field
# from typing import Optional
# from datetime import datetime


# class ClientCreate(BaseModel):
#     business_name: str = Field(..., min_length=1)
#     niche: str = "restaurant"
#     phone: Optional[str] = None
#     address: Optional[str] = None
#     email: Optional[EmailStr] = None
#     city: Optional[str] = None
#     state: Optional[str] = None
#     rating: Optional[str] = None
#     google_maps_url: Optional[str] = None
#     facebook_url: Optional[str] = None
#     instagram_url: Optional[str] = None
#     lead_score: Optional[str] = None


# class ClientResponse(BaseModel):
#     id: int
#     slug: str
#     business_name: str
#     niche: str
#     phone: Optional[str] = None
#     address: Optional[str] = None
#     email: Optional[str] = None
#     city: Optional[str] = None
#     state: Optional[str] = None
#     rating: Optional[str] = None
#     google_maps_url: Optional[str] = None
#     facebook_url: Optional[str] = None
#     instagram_url: Optional[str] = None
#     lead_score: Optional[str] = None
#     demo_url: Optional[str] = None
#     created_at: datetime
#     updated_at: datetime

#     class Config:
#         from_attributes = True


# # app/schemas.py (append)

# class AppointmentCreate(BaseModel):
#     name: str = Field(..., min_length=1)
#     phone: str = Field(..., min_length=8)
#     email: EmailStr
#     service: str = Field(..., min_length=1)
#     date: str
#     time: str
#     notes: Optional[str] = ""


# class AppointmentResponse(BaseModel):
#     success: bool
#     bookingId: str
#     message: Optional[str] = None

# backend/app/schemas.py

# from pydantic import BaseModel, EmailStr, Field
# from typing import Optional
# from datetime import datetime


# class ClientCreate(BaseModel):
#     business_name: str = Field(..., min_length=1)
#     niche: str = "restaurant"
#     phone: Optional[str] = None
#     address: Optional[str] = None
#     email: Optional[EmailStr] = None
#     city: Optional[str] = None
#     state: Optional[str] = None
#     rating: Optional[str] = None
#     google_maps_url: Optional[str] = None
#     facebook_url: Optional[str] = None
#     instagram_url: Optional[str] = None
#     lead_score: Optional[str] = None
#     latitude: Optional[str] = None
#     longitude: Optional[str] = None
#     id: int
#     slug: str
#     business_name: str
#     niche: str
#     phone: Optional[str] = None
#     address: Optional[str] = None
#     email: Optional[str] = None
#     city: Optional[str] = None
#     state: Optional[str] = None
#     rating: Optional[str] = None
#     google_maps_url: Optional[str] = None
#     facebook_url: Optional[str] = None
#     instagram_url: Optional[str] = None
#     lead_score: Optional[str] = None
#     latitude: Optional[str] = None
#     longitude: Optional[str] = None
#     demo_url: Optional[str] = None
#     created_at: datetime
#     updated_at: datetime

#     class Config:
#         from_attributes = True


# # app/schemas.py (append)

# class AppointmentCreate(BaseModel):
#     name: str = Field(..., min_length=1)
#     phone: str = Field(..., min_length=8)
#     email: EmailStr
#     service: str = Field(..., min_length=1)
#     date: str
#     time: str
#     notes: Optional[str] = ""


# class AppointmentResponse(BaseModel):
#     success: bool
#     bookingId: str
#     message: Optional[str] = None

# backend/app/schemas.py
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class ClientCreate(BaseModel):
    business_name: str = Field(..., min_length=1)
    niche: str = "restaurant"
    phone: Optional[str] = None
    address: Optional[str] = None
    email: Optional[EmailStr] = None
    city: Optional[str] = None
    state: Optional[str] = None
    rating: Optional[str] = None
    google_maps_url: Optional[str] = None
    facebook_url: Optional[str] = None
    instagram_url: Optional[str] = None
    lead_score: Optional[str] = None
    latitude: Optional[str] = None
    longitude: Optional[str] = None


class ClientResponse(BaseModel):
    id: int
    slug: str
    business_name: str
    niche: str
    phone: Optional[str] = None
    address: Optional[str] = None
    email: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    rating: Optional[str] = None
    google_maps_url: Optional[str] = None
    facebook_url: Optional[str] = None
    instagram_url: Optional[str] = None
    lead_score: Optional[str] = None
    latitude: Optional[str] = None
    longitude: Optional[str] = None
    demo_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# app/schemas.py (append)

class AppointmentCreate(BaseModel):
    name: str = Field(..., min_length=1)
    phone: str = Field(..., min_length=8)
    email: EmailStr
    service: str = Field(..., min_length=1)
    date: str
    time: str
    notes: Optional[str] = ""


class AppointmentResponse(BaseModel):
    success: bool
    bookingId: str
    message: Optional[str] = None