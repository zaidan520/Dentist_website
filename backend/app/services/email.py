import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import logging

logger = logging.getLogger(__name__)

def build_email_html(booking_details: dict, booking_id: str) -> str:
    # (same as before, keep it)
    return f"""
    <div style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; border: 1px solid #e5e7eb; border-radius: 8px; overflow: hidden;">
      <div style="background-color: #1e293b; padding: 20px; text-align: center;">
        <h1 style="color: #ffffff; margin: 0; font-size: 20px;">DENTAL HEALTH CLINIC</h1>
        <p style="color: #0f766e; margin: 5px 0 0 0; font-size: 12px; font-weight: bold; letter-spacing: 1px;">NEW APPOINTMENT REQUEST</p>
      </div>
      <div style="padding: 24px; background-color: #ffffff;">
        <p style="margin-top: 0;">Hello Clinic Team,</p>
        <p>A new appointment request has been received from the website. Details are listed below:</p>
        <table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
          <tr style="border-bottom: 1px solid #f3f4f6;">
            <td style="padding: 8px 0; font-weight: bold; color: #4b5563; width: 140px;">Booking Ref:</td>
            <td style="padding: 8px 0; font-weight: bold; color: #111827;">{booking_id}</td>
          </tr>
          <tr style="border-bottom: 1px solid #f3f4f6;">
            <td style="padding: 8px 0; font-weight: bold; color: #4b5563;">Patient Name:</td>
            <td style="padding: 8px 0; color: #111827;">{booking_details.get('name', '')}</td>
          </tr>
          <tr style="border-bottom: 1px solid #f3f4f6;">
            <td style="padding: 8px 0; font-weight: bold; color: #4b5563;">Phone Number:</td>
            <td style="padding: 8px 0; color: #111827;"><a href="tel:{booking_details.get('phone', '')}">{booking_details.get('phone', '')}</a></td>
          </tr>
          <tr style="border-bottom: 1px solid #f3f4f6;">
            <td style="padding: 8px 0; font-weight: bold; color: #4b5563;">Email Address:</td>
            <td style="padding: 8px 0; color: #111827;"><a href="mailto:{booking_details.get('email', '')}">{booking_details.get('email', '')}</a></td>
          </tr>
          <tr style="border-bottom: 1px solid #f3f4f6;">
            <td style="padding: 8px 0; font-weight: bold; color: #4b5563;">Selected Service:</td>
            <td style="padding: 8px 0; color: #111827; font-weight: bold;">{booking_details.get('service', '')}</td>
          </tr>
          <tr style="border-bottom: 1px solid #f3f4f6;">
            <td style="padding: 8px 0; font-weight: bold; color: #4b5563;">Preferred Date:</td>
            <td style="padding: 8px 0; color: #111827;">{booking_details.get('date', '')}</td>
          </tr>
          <tr style="border-bottom: 1px solid #f3f4f6;">
            <td style="padding: 8px 0; font-weight: bold; color: #4b5563;">Preferred Time:</td>
            <td style="padding: 8px 0; color: #111827;">{booking_details.get('time', '')}</td>
          </tr>
          <tr>
            <td style="padding: 8px 0; font-weight: bold; color: #4b5563; vertical-align: top;">Optional Notes:</td>
            <td style="padding: 8px 0; color: #4b5563; font-style: italic;">{booking_details.get('notes', 'No additional notes provided.')}</td>
          </tr>
        </table>
        <p style="background-color: #f3f4f6; padding: 12px; border-radius: 6px; font-size: 13px; text-align: center; color: #4b5563; margin-bottom: 0;">
          <strong>Action Required:</strong> Please contact the patient at the listed number to confirm their slot.
        </p>
      </div>
      <div style="background-color: #f9fafb; padding: 16px; text-align: center; font-size: 11px; color: #9ca3af; border-top: 1px solid #e5e7eb;">
        This email contains a generated PDF transcript of the booking request.
      </div>
    </div>
    """

# def send_appointment_email(booking_details: dict, booking_id: str, pdf_bytes: bytes) -> dict:
#     smtp_host = os.getenv("SMTP_HOST")
#     smtp_port = int(os.getenv("SMTP_PORT", 587))
#     smtp_user = os.getenv("SMTP_USER")
#     smtp_password = os.getenv("SMTP_PASSWORD")
#     clinic_email = os.getenv("CLINIC_EMAIL", "clinic@example.com")

#     # Log what we have (for debugging)
#     logger.info(f"SMTP settings: host={smtp_host}, port={smtp_port}, user={smtp_user}, password={smtp_password[:4]}..., clinic={clinic_email}")

#     if not smtp_user or not smtp_password:
#         logger.warning("SMTP credentials missing, dry-run mode.")
#         return {"success": True, "simulated": True}

#     try:
#         msg = MIMEMultipart()
#         msg["From"] = smtp_user
#         msg["To"] = clinic_email
#         msg["Subject"] = f"New Appointment Request - {booking_details.get('name', '')} [Ref: {booking_id}]"

#         html_content = build_email_html(booking_details, booking_id)
#         msg.attach(MIMEText(html_content, "html"))

#         pdf_attachment = MIMEApplication(pdf_bytes, _subtype="pdf")
#         pdf_attachment.add_header(
#             "Content-Disposition",
#             f"attachment; filename=appointment_{booking_id}.pdf"
#         )
#         msg.attach(pdf_attachment)

#         with smtplib.SMTP(smtp_host, smtp_port) as server:
#             server.starttls()
#             server.login(smtp_user, smtp_password)
#             server.send_message(msg)

#         logger.info(f"✅ Email sent successfully to {clinic_email}")
#         return {"success": True, "simulated": False}

#     except Exception as e:
#         logger.error(f"❌ SMTP send failed: {e}")
#         # Return error so the API can handle it (or just log)
#         raise

def send_appointment_email(booking_details: dict, booking_id: str, pdf_bytes: bytes) -> dict:
    smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", 587))  # keep 587 for STARTTLS, or 465 for SSL
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")
    clinic_email = os.getenv("CLINIC_EMAIL", "clinic@example.com")

    if not smtp_user or not smtp_password:
        logger.warning("SMTP credentials missing, dry‑run mode.")
        return {"success": True, "simulated": True}

    try:
        # Outer container: mixed (for attachments + alternatives)
        outer = MIMEMultipart('mixed')
        outer["From"] = f'"Dental Health Web" <{smtp_user}>'
        outer["To"] = clinic_email
        outer["Subject"] = f"New Appointment Request - {booking_details.get('name', '')} [Ref: {booking_id}]"
        outer["Reply-To"] = booking_details.get('email', smtp_user)

        # Inner container: alternative (plain + html)
        alt = MIMEMultipart('alternative')
        plain_text = f"""
NEW APPOINTMENT REQUEST
Ref: {booking_id}

Patient: {booking_details.get('name', '')}
Phone: {booking_details.get('phone', '')}
Service: {booking_details.get('service', '')}
Date: {booking_details.get('date', '')}
Time: {booking_details.get('time', '')}
Notes: {booking_details.get('notes', 'No additional notes provided.')}

Please contact the patient to confirm the slot.
        """
        alt.attach(MIMEText(plain_text, "plain"))
        html_content = build_email_html(booking_details, booking_id)
        alt.attach(MIMEText(html_content, "html"))
        outer.attach(alt)

        # PDF attachment
        pdf_attachment = MIMEApplication(pdf_bytes, _subtype="pdf")
        pdf_attachment.add_header(
            "Content-Disposition",
            f"attachment; filename=appointment_{booking_id}.pdf"
        )
        outer.attach(pdf_attachment)

        # Send
        if smtp_port == 465:
            # SSL connection
            with smtplib.SMTP_SSL(smtp_host, smtp_port) as server:
                server.login(smtp_user, smtp_password)
                server.send_message(outer)
        else:
            # STARTTLS (587)
            with smtplib.SMTP(smtp_host, smtp_port) as server:
                server.starttls()
                server.login(smtp_user, smtp_password)
                server.send_message(outer)

        logger.info(f"✅ Email sent successfully to {clinic_email}")
        return {"success": True, "simulated": False}

    except Exception as e:
        logger.error(f"❌ SMTP send failed: {e}")
        raise