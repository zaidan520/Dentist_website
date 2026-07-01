# app/services/whatsapp.py
import os
import logging
import httpx

logger = logging.getLogger(__name__)

def send_appointment_whatsapp(booking_details: dict, booking_id: str) -> dict:
    whatsapp_api_key = os.getenv("WHATSAPP_API_KEY")
    whatsapp_phone = os.getenv("WHATSAPP_PHONE_NUMBER", "+15550199")
    webhook_url = os.getenv("WHATSAPP_WEBHOOK_URL")

    # Build message
    message_body = f"""*NEW APPOINTMENT REQUEST*
Ref: {booking_id}

• *Patient:* {booking_details.get('name', '')}
• *Phone:* {booking_details.get('phone', '')}
• *Service:* {booking_details.get('service', '')}
• *Date:* {booking_details.get('date', '')}
• *Time:* {booking_details.get('time', '')}

Please contact the patient to confirm the slot."""

    try:
        # Webhook
        if webhook_url:
            logger.info("Forwarding WhatsApp via webhook")
            headers = {"Content-Type": "application/json"}
            if whatsapp_api_key:
                headers["Authorization"] = f"Bearer {whatsapp_api_key}"
            payload = {
                "phone": whatsapp_phone,
                "message": message_body,
                "ref": booking_id
            }
            with httpx.Client() as client:
                response = client.post(webhook_url, json=payload, headers=headers)
                response.raise_for_status()
            logger.info("WhatsApp webhook successful")
            return {"success": True, "method": "webhook"}

        # Twilio
        twilio_sid = os.getenv("TWILIO_ACCOUNT_SID")
        twilio_auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        twilio_from = os.getenv("TWILIO_WHATSAPP_FROM", "whatsapp:+14155238886")

        if twilio_sid and twilio_auth_token:
            logger.info("Sending WhatsApp via Twilio")
            url = f"https://api.twilio.com/2010-04-01/Accounts/{twilio_sid}/Messages.json"
            auth = (twilio_sid, twilio_auth_token)
            data = {
                "To": f"whatsapp:{whatsapp_phone}",
                "From": twilio_from,
                "Body": message_body
            }
            with httpx.Client() as client:
                response = client.post(url, data=data, auth=auth)
                response.raise_for_status()
            logger.info("Twilio WhatsApp sent")
            return {"success": True, "method": "twilio"}

        # Dry-run
        logger.warning("WhatsApp credentials not configured, dry-run mode")
        print("\n--- WHATSAPP NOTIFICATION LOG TRACE (DRY-RUN) ---")
        print(f"To: {whatsapp_phone}")
        print(f"Body:\n{message_body}")
        print("--------------------------------------------------\n")
        return {"success": True, "method": "dry-run"}

    except Exception as e:
        logger.error(f"WhatsApp send failed: {e}")
        return {"success": False, "error": str(e)}