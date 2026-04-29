"""
Generate starter fixture PDFs for the eval dataset.
Run once: uv run python eval/datasets/generate_fixtures.py
from the repo root (backend venv provides pymupdf).
"""

from pathlib import Path

import pymupdf

FIXTURES = {
    "invoice_01.pdf": (
        "INVOICE\n"
        "Invoice No: INV-2025-001\n"
        "Date: 2025-01-15\n"
        "Bill To: BPCL Corp, Mumbai\n\n"
        "Description: Consulting Services - January 2025\n"
        "Quantity: 1    Unit Price: $5,000.00\n"
        "Subtotal: $5,000.00\n"
        "Tax (18%): $900.00\n"
        "Total Due: $5,900.00\n\n"
        "Payment Terms: Net 30\n"
        "Bank: HDFC Bank  Account No: 123456789  IFSC: HDFC0001234\n"
    ),
    "contract_01.pdf": (
        "SERVICE AGREEMENT\n\n"
        "This Agreement is entered into as of January 1, 2025 between:\n"
        "Party A: Acme Technologies Pvt Ltd (hereinafter 'Service Provider')\n"
        "Party B: BPCL Ltd (hereinafter 'Client')\n\n"
        "1. Scope of Services\n"
        "   Service Provider agrees to deliver software development services.\n\n"
        "2. Term and Termination\n"
        "   This Agreement commences on 01-Jan-2025 and ends on 31-Dec-2025.\n\n"
        "3. Confidentiality\n"
        "   Both parties agree to maintain strict confidentiality.\n\n"
        "4. Payment Terms\n"
        "   Client shall pay within 30 days of invoice receipt.\n\n"
        "Signed:\n"
        "Party A: ___________    Date: ___________\n"
        "Party B: ___________    Date: ___________\n"
    ),
    "id_proof_01.pdf": (
        "GOVERNMENT OF INDIA\n"
        "PERMANENT ACCOUNT NUMBER CARD\n\n"
        "Name: JOHN DOE\n"
        "Father's Name: JAMES DOE\n"
        "Date of Birth: 01/01/1985\n"
        "PAN: ABCDE1234F\n\n"
        "Issued by Income Tax Department\n"
        "This card is the property of the Government of India.\n"
        "Signature: ___________\n"
    ),
    "report_01.pdf": (
        "QUARTERLY PERFORMANCE REPORT — Q4 2025\n\n"
        "Prepared by: Strategy & Analytics Team\n"
        "Date: January 10, 2026\n\n"
        "Executive Summary\n"
        "Revenue: $12.5M (+15% YoY)\n"
        "Operating Profit: $3.2M (+8% YoY)\n\n"
        "Key Highlights\n"
        "- New product line launched in October 2025\n"
        "- Market share increased from 12% to 14%\n"
        "- Customer satisfaction score: 4.3/5\n\n"
        "Recommendations for Q1 2026\n"
        "1. Expand distribution in tier-2 cities\n"
        "2. Invest in digital marketing\n"
        "3. Review operational costs\n"
    ),
    "other_01.pdf": (
        "MEETING NOTES — Project Sync\n"
        "Date: March 15, 2025\n"
        "Attendees: John (PM), Jane (Dev Lead), Bob (QA)\n\n"
        "Discussion Points\n"
        "- Sprint 3 velocity was lower than expected\n"
        "- Blocker: API integration delayed by vendor\n\n"
        "Action Items\n"
        "1. John: Review and update timeline by Friday\n"
        "2. Jane: Coordinate with vendor on API specs\n"
        "3. Bob: Prepare regression test plan\n\n"
        "Next Meeting: March 22, 2025 at 10:00 AM\n"
    ),
}

EXPECTED = {
    "invoice_01.pdf": "invoice",
    "contract_01.pdf": "contract",
    "id_proof_01.pdf": "id_proof",
    "report_01.pdf": "report",
    "other_01.pdf": "other",
}

out_dir = Path(__file__).parent / "fixtures"
out_dir.mkdir(exist_ok=True)

for filename, text in FIXTURES.items():
    path = out_dir / filename
    doc = pymupdf.open()
    page = doc.new_page()
    page.insert_text((72, 72), text, fontsize=11)
    doc.save(str(path))
    doc.close()
    print(f"  wrote {path}")

print("done — fixtures generated.")
