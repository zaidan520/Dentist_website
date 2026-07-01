# # app/routes/appointments.py
# from fastapi import APIRouter, HTTPException, Query, Request
# from fastapi.responses import Response
# from ..schemas import AppointmentCreate, AppointmentResponse
# from ..services.pdf import generate_booking_pdf
# from ..services.email import send_appointment_email
# from ..services.whatsapp import send_appointment_whatsapp
# import random
# import logging
# from datetime import datetime

# router = APIRouter(prefix="/api/appointments", tags=["appointments"])

# def generate_booking_id():
#     return f"B-{random.randint(10000, 99999)}"

# def validate_appointment(data: dict):
#     # Replicate validation from your Express middleware
#     # Simple checks: name, phone, email, service, date, time present
#     required = ["name", "phone", "email", "service", "date", "time"]
#     for field in required:
#         if not data.get(field):
#             raise HTTPException(status_code=400, detail=f"Missing required field: {field}")

#     # Email format
#     import re
#     email_pattern = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
#     if not re.match(email_pattern, data["email"]):
#         raise HTTPException(status_code=400, detail="Invalid email format")

#     # Phone format (simple)
#     phone_pattern = r'^[\d\s()+-]{8,20}$'
#     if not re.match(phone_pattern, data["phone"]):
#         raise HTTPException(status_code=400, detail="Invalid phone number")

#     # Date must be in future
#     try:
#         appointment_date = datetime.strptime(data["date"], "%Y-%m-%d").date()
#         today = datetime.now().date()
#         if appointment_date <= today:
#             raise HTTPException(status_code=400, detail="Date must be in the future")
#     except ValueError:
#         raise HTTPException(status_code=400, detail="Invalid date format (use YYYY-MM-DD)")

#     # Time must be non-empty
#     if not data["time"]:
#         raise HTTPException(status_code=400, detail="Time is required")

#     # Strip HTML tags (basic)
#     for field in ["name", "phone", "email", "service", "date", "time", "notes"]:
#         if data.get(field):
#             data[field] = data[field].strip()
#     return data

# @router.post("/")
# async def book_appointment(request: Request, appointment: AppointmentCreate):
#     # Convert to dict
#     booking_data = appointment.dict()
#     # Validate manually (or we can use Pydantic validators)
#     try:
#         validated = validate_appointment(booking_data)
#     except HTTPException as e:
#         raise e

#     booking_id = generate_booking_id()

#     # Generate PDF
#     try:
#         pdf_bytes = generate_booking_pdf(validated, booking_id)
#     except Exception as e:
#         logging.error(f"PDF generation failed: {e}")
#         raise HTTPException(status_code=500, detail="PDF generation error")

#     # Send email
#     try:
#         email_result = send_appointment_email(validated, booking_id, pdf_bytes)
#         logging.info(f"Email result: {email_result}")
#     except Exception as e:
#         logging.error(f"Email send failed: {e}")
#         # We don't fail the whole request

#     # Send WhatsApp
#     try:
#         whatsapp_result = send_appointment_whatsapp(validated, booking_id)
#         logging.info(f"WhatsApp result: {whatsapp_result}")
#     except Exception as e:
#         logging.error(f"WhatsApp send failed: {e}")

#     return {
#         "success": True,
#         "bookingId": booking_id,
#         "message": "Appointment request sent successfully."
#     }
# # from ..services.email import send_appointment_email

# def send_appointment_email(booking_details, booking_id, pdf_bytes):
#     print(f"Email would be sent for booking {booking_id}")
#     return {"success": True, "simulated": True}

# @router.get("/download-pdf")
# async def download_booking_pdf(
#     name: str = Query(...),
#     phone: str = Query(...),
#     email: str = Query(...),
#     service: str = Query(...),
#     date: str = Query(...),
#     time: str = Query(...),
#     notes: str = Query("")
# ):
#     # Build booking details
#     booking_details = {
#         "name": name,
#         "phone": phone,
#         "email": email,
#         "service": service,
#         "date": date,
#         "time": time,
#         "notes": notes
#     }
#     # Validate similar to above (simplified)
#     try:
#         validate_appointment(booking_details)
#     except HTTPException as e:
#         raise e

#     booking_id = "TEMP-DL"
#     pdf_bytes = generate_booking_pdf(booking_details, booking_id)
#     filename = f"appointment_{name.replace(' ', '_')}.pdf"
#     return Response(
#         content=pdf_bytes,
#         media_type="application/pdf",
#         headers={"Content-Disposition": f"attachment; filename={filename}"}
#     )
# app/routes/appointments.py
from fastapi import APIRouter, HTTPException, Query, Request
from fastapi.responses import Response
from ..schemas import AppointmentCreate, AppointmentResponse
from ..services.pdf import generate_booking_pdf
from ..services.email import send_appointment_email
from ..services.whatsapp import send_appointment_whatsapp
import random
import logging
from datetime import datetime

router = APIRouter(prefix="/api/appointments", tags=["appointments"])

def generate_booking_id():
    return f"B-{random.randint(10000, 99999)}"

def validate_appointment(data: dict):
    # Replicate validation from your Express middleware
    # Simple checks: name, phone, email, service, date, time present
    required = ["name", "phone", "email", "service", "date", "time"]
    for field in required:
        if not data.get(field):
            raise HTTPException(status_code=400, detail=f"Missing required field: {field}")

    # Email format
    import re
    email_pattern = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
    if not re.match(email_pattern, data["email"]):
        raise HTTPException(status_code=400, detail="Invalid email format")

    # Phone format (simple)
    phone_pattern = r'^[\d\s()+-]{8,20}$'
    if not re.match(phone_pattern, data["phone"]):
        raise HTTPException(status_code=400, detail="Invalid phone number")

    # Date must be in future
    try:
        appointment_date = datetime.strptime(data["date"], "%Y-%m-%d").date()
        today = datetime.now().date()
        if appointment_date <= today:
            raise HTTPException(status_code=400, detail="Date must be in the future")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format (use YYYY-MM-DD)")

    # Time must be non-empty
    if not data["time"]:
        raise HTTPException(status_code=400, detail="Time is required")

    # Strip HTML tags (basic)
    for field in ["name", "phone", "email", "service", "date", "time", "notes"]:
        if data.get(field):
            data[field] = data[field].strip()
    return data

@router.post("/")
async def book_appointment(request: Request, appointment: AppointmentCreate):
    # Convert to dict
    booking_data = appointment.dict()
    # Validate manually (or we can use Pydantic validators)
    try:
        validated = validate_appointment(booking_data)
    except HTTPException as e:
        raise e

    booking_id = generate_booking_id()

    # Generate PDF
    try:
        pdf_bytes = generate_booking_pdf(validated, booking_id)
    except Exception as e:
        logging.error(f"PDF generation failed: {e}")
        raise HTTPException(status_code=500, detail="PDF generation error")

    # Send email
    try:
        email_result = send_appointment_email(validated, booking_id, pdf_bytes)
        logging.info(f"Email result: {email_result}")
    except Exception as e:
        logging.error(f"Email send failed: {e}")
        # We don't fail the whole request

    # Send WhatsApp
    try:
        whatsapp_result = send_appointment_whatsapp(validated, booking_id)
        logging.info(f"WhatsApp result: {whatsapp_result}")
    except Exception as e:
        logging.error(f"WhatsApp send failed: {e}")

    return {
        "success": True,
        "bookingId": booking_id,
        "message": "Appointment request sent successfully."
    }

@router.get("/download-pdf")
async def download_booking_pdf(
    name: str = Query(...),
    phone: str = Query(...),
    email: str = Query(...),
    service: str = Query(...),
    date: str = Query(...),
    time: str = Query(...),
    notes: str = Query("")
):
    # Build booking details
    booking_details = {
        "name": name,
        "phone": phone,
        "email": email,
        "service": service,
        "date": date,
        "time": time,
        "notes": notes
    }
    # Validate similar to above (simplified)
    try:
        validate_appointment(booking_details)
    except HTTPException as e:
        raise e

    booking_id = "TEMP-DL"
    pdf_bytes = generate_booking_pdf(booking_details, booking_id)
    filename = f"appointment_{name.replace(' ', '_')}.pdf"
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )