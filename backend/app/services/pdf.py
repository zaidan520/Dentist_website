# app/services/pdf.py
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from io import BytesIO
import datetime

def generate_booking_pdf(booking_details: dict, booking_id: str) -> bytes:
    """
    Returns PDF as bytes.
    """
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Colors
    primary_color = (0.118, 0.161, 0.231)   # #1e293b
    accent_color = (0.059, 0.463, 0.431)    # #0f766e
    text_dark = (0.2, 0.204, 0.235)         # #334155
    light_gray = (0.796, 0.827, 0.882)      # #cbd5e1

    # Header
    c.setFillColorRGB(*primary_color)
    c.setFont("Helvetica-Bold", 24)
    c.drawString(50*mm, height - 50*mm, "DENTAL HEALTH")
    c.setFillColorRGB(*accent_color)
    c.setFont("Helvetica", 9)
    c.drawString(52*mm, height - 75*mm, "QUALITY HEALTHCARE SERVICES")

    # Metadata (right)
    submit_date = datetime.datetime.now().strftime("%B %d, %Y at %I:%M %p")
    c.setFillColorRGB(*text_dark)
    c.setFont("Helvetica", 9)
    c.drawRightString(width - 50*mm, height - 50*mm, f"Booking Ref: {booking_id}")
    c.drawRightString(width - 50*mm, height - 65*mm, f"Submitted: {submit_date}")

    # Divider
    c.setStrokeColorRGB(0.796, 0.827, 0.882)
    c.setLineWidth(1)
    c.line(50*mm, height - 100*mm, width - 50*mm, height - 100*mm)

    # Title
    c.setFillColorRGB(*primary_color)
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width/2, height - 120*mm, "APPOINTMENT BOOKING TRANSCRIPT")
    c.setFillColorRGB(*text_dark)
    c.setFont("Helvetica", 10)
    c.drawCentredString(width/2, height - 135*mm, "A request has been submitted to the clinic. Our representative will contact the patient to confirm.")

    # Grid positions
    start_y = height - 160*mm
    col1_x = 50*mm
    col2_x = 300*mm
    row_height = 20*mm

    # Headers
    c.setFillColorRGB(*primary_color)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(col1_x, start_y, "Patient Details")
    c.drawString(col2_x, start_y, "Appointment Details")

    # Underlines
    c.setStrokeColorRGB(*accent_color)
    c.setLineWidth(1.5)
    c.line(col1_x, start_y - 5*mm, col1_x + 200*mm, start_y - 5*mm)
    c.line(col2_x, start_y - 5*mm, col2_x + 245*mm, start_y - 5*mm)

    # Patient info (left)
    y_pos = start_y - 25*mm
    c.setFillColorRGB(*text_dark)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(col1_x, y_pos, "Name:")
    c.setFont("Helvetica", 10)
    c.drawString(col1_x + 60*mm, y_pos, booking_details.get('name', ''))

    y_pos -= row_height
    c.setFont("Helvetica-Bold", 10)
    c.drawString(col1_x, y_pos, "Phone:")
    c.setFont("Helvetica", 10)
    c.drawString(col1_x + 60*mm, y_pos, booking_details.get('phone', ''))

    y_pos -= row_height
    c.setFont("Helvetica-Bold", 10)
    c.drawString(col1_x, y_pos, "Email:")
    c.setFont("Helvetica", 10)
    c.drawString(col1_x + 60*mm, y_pos, booking_details.get('email', ''))

    # Appointment info (right)
    y_pos = start_y - 25*mm
    c.setFont("Helvetica-Bold", 10)
    c.drawString(col2_x, y_pos, "Service:")
    c.setFont("Helvetica", 10)
    c.drawString(col2_x + 60*mm, y_pos, booking_details.get('service', ''))

    y_pos -= row_height
    c.setFont("Helvetica-Bold", 10)
    c.drawString(col2_x, y_pos, "Date:")
    c.setFont("Helvetica", 10)
    c.drawString(col2_x + 60*mm, y_pos, booking_details.get('date', ''))

    y_pos -= row_height
    c.setFont("Helvetica-Bold", 10)
    c.drawString(col2_x, y_pos, "Time:")
    c.setFont("Helvetica", 10)
    c.drawString(col2_x + 60*mm, y_pos, booking_details.get('time', ''))

    # Notes section
    notes_y = start_y - 80*mm
    c.setFillColorRGB(*primary_color)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(col1_x, notes_y, "Optional Patient Notes")
    c.setStrokeColorRGB(0.796, 0.827, 0.882)
    c.setLineWidth(1)
    c.line(col1_x, notes_y - 5*mm, width - 50*mm, notes_y - 5*mm)

    notes_text = booking_details.get('notes', 'No additional notes provided.')
    c.setFillColorRGB(*text_dark)
    c.setFont("Helvetica", 10)
    text_object = c.beginText(col1_x, notes_y - 25*mm)
    text_object.setFont("Helvetica", 10)
    # Split lines manually
    from reportlab.lib.utils import simpleSplit
    lines = simpleSplit(notes_text, "Helvetica", 10, width - 100*mm)
    for line in lines:
        text_object.textLine(line)
    c.drawText(text_object)

    # Footer
    footer_y = 30*mm
    c.setStrokeColorRGB(0.886, 0.910, 0.941)
    c.setLineWidth(1)
    c.line(50*mm, footer_y + 10*mm, width - 50*mm, footer_y + 10*mm)

    c.setFillColorRGB(0.58, 0.64, 0.72)
    c.setFont("Helvetica-Oblique", 8)
    c.drawCentredString(width/2, footer_y, "This is a simulated dental clinic appointment confirmation PDF. All data listed here is for placeholder/demo purposes.")

    c.setFillColorRGB(0.392, 0.463, 0.545)
    c.setFont("Helvetica", 9)
    c.drawCentredString(width/2, footer_y - 10*mm, "Dental Health Inc. • 600 Palisade Ave, West New York, NJ • +1 (555) 0199")

    c.save()
    return buffer.getvalue()