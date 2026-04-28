from app.services.pdf_router import route


def test_routes_text_pdf_as_text(text_pdf_bytes: bytes):
    assert route(text_pdf_bytes, "application/pdf") == "text"


def test_routes_blank_pdf_as_image(image_pdf_bytes: bytes):
    assert route(image_pdf_bytes, "application/pdf") == "image"


def test_image_content_type_short_circuits_without_reading_bytes():
    assert route(b"", "image/png") == "image"
    assert route(b"", "image/jpeg") == "image"
