import io

import pymupdf
import pytest
from PIL import Image, ImageDraw, ImageFont


@pytest.fixture
def text_pdf_bytes() -> bytes:
    """A PDF with embedded text — should route as 'text'."""
    doc = pymupdf.open()
    page = doc.new_page()
    page.insert_text(
        (72, 72),
        (
            "INVOICE No. 12345\n"
            "Bill To: Acme Corp, 123 Main Street, Springfield\n"
            "Total Due: $1,234.56\n"
            "Tax (10%): $123.45\n"
            "Due Date: 2026-05-01\n"
            "Payment Terms: Net 30\n"
        ),
        fontsize=12,
    )
    out = doc.tobytes()
    doc.close()
    return out


@pytest.fixture
def image_pdf_bytes() -> bytes:
    """A PDF with no embedded text — should route as 'image'."""
    doc = pymupdf.open()
    doc.new_page()  # blank page, zero embedded text
    out = doc.tobytes()
    doc.close()
    return out


@pytest.fixture
def text_image_bytes() -> bytes:
    """A large PNG with rendered text — usable input to OCR."""
    img = Image.new("RGB", (1200, 400), color="white")
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("arial.ttf", 80)
    except OSError:
        font = ImageFont.load_default()
    draw.text((40, 140), "INVOICE 12345", fill="black", font=font)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()
