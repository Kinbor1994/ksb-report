"""
KSB-Report — Invoice Template
Pre-built template helper for generating invoices.
"""

from __future__ import annotations

from datetime import datetime

from ksb_report.schemas import (
    FooterConfig,
    HeaderConfig,
    HeaderLine,
    KeyValueElement,
    PageConfig,
    ReportTemplate,
    SectionTitleElement,
    SpacerElement,
    TableElement,
    TextElement,
)


def invoice_template(
    *,
    company_name: str,
    company_logo: str | None = None,
    invoice_number: str,
    invoice_date: str | None = None,
    due_date: str | None = None,
    client_name: str,
    client_address: str = "",
    client_email: str = "",
    items: list[dict],
    currency: str = "€",
    tax_rate: float = 0.0,
    notes: str = "",
    header_color: tuple[int, int, int] = (41, 128, 185),
) -> ReportTemplate:
    """
    Build a ready-to-use invoice ReportTemplate.

    Args:
        company_name: Your company name
        company_logo: Path to company logo (optional)
        invoice_number: Unique invoice identifier
        invoice_date: Date of invoice (defaults to today)
        due_date: Payment due date (optional)
        client_name: Client / customer name
        client_address: Client address
        client_email: Client email
        items: List of dicts with keys: description, quantity, unit_price
        currency: Currency symbol (default: €)
        tax_rate: Tax rate as decimal (0.18 = 18%)
        notes: Additional notes shown at the bottom
        header_color: RGB color for table headers

    Returns:
        A ReportTemplate ready to be passed to ReportEngine.generate()
    """
    if not invoice_date:
        invoice_date = datetime.now().strftime("%d/%m/%Y")

    # Build table rows with calculated totals
    table_rows: list[list[str]] = []
    subtotal = 0.0
    for i, item in enumerate(items, 1):
        qty = item.get("quantity", 1)
        price = item.get("unit_price", 0.0)
        total = qty * price
        subtotal += total
        table_rows.append(
            [
                str(i),
                item.get("description", ""),
                str(qty),
                f"{price:,.2f} {currency}",
                f"{total:,.2f} {currency}",
            ]
        )

    tax_amount = subtotal * tax_rate
    grand_total = subtotal + tax_amount

    # Build elements
    elements = []

    # Invoice metadata
    elements.append(SpacerElement(height=5))
    elements.append(
        KeyValueElement(
            pairs=[
                ("Facture N°", invoice_number),
                ("Date", invoice_date),
                *([("Échéance", due_date)] if due_date else []),
            ],
            label_width=35,
            font_size=11,
        )
    )

    elements.append(SpacerElement(height=5))

    # Client info
    elements.append(
        SectionTitleElement(
            text="CLIENT",
            bg_color=(240, 240, 240),
        )
    )
    client_info_pairs = [("Nom", client_name)]
    if client_address:
        client_info_pairs.append(("Adresse", client_address))
    if client_email:
        client_info_pairs.append(("Email", client_email))
    elements.append(
        KeyValueElement(
            pairs=client_info_pairs,
            label_width=30,
            font_size=10,
        )
    )

    elements.append(SpacerElement(height=5))

    # Items table
    elements.append(
        SectionTitleElement(
            text="ARTICLES",
            bg_color=(240, 240, 240),
        )
    )
    elements.append(
        TableElement(
            headers=["#", "Description", "Qté", "Prix unitaire", "Total"],
            rows=table_rows,
            column_widths=[8, 45, 10, 18, 19],
            header_bg_color=header_color,
            header_text_color=(255, 255, 255),
            striped_rows=True,
            font_size=10,
            header_font_size=10,
        )
    )

    # Totals
    elements.append(SpacerElement(height=3))
    total_pairs = [("Sous-total", f"{subtotal:,.2f} {currency}")]
    if tax_rate > 0:
        total_pairs.append(
            (f"TVA ({tax_rate * 100:.0f}%)", f"{tax_amount:,.2f} {currency}")
        )
    total_pairs.append(("TOTAL TTC", f"{grand_total:,.2f} {currency}"))
    elements.append(
        KeyValueElement(
            pairs=total_pairs,
            label_width=50,
            font_size=12,
            bold_labels=True,
        )
    )

    # Notes
    if notes:
        elements.append(SpacerElement(height=10))
        elements.append(SectionTitleElement(text="NOTES", bg_color=(240, 240, 240)))
        elements.append(TextElement(content=notes, font_size=10, font_style="I"))

    # Build header
    header_lines = [
        HeaderLine(text=company_name, font_size=16, bold=True),
    ]
    header = HeaderConfig(
        lines=header_lines,
        logo_left=company_logo,
        separator_line=True,
    )

    return ReportTemplate(
        title=f"FACTURE {invoice_number}",
        title_font_size=16,
        page=PageConfig(orientation="portrait", format="A4"),
        header=header,
        footer=FooterConfig(
            left_text=f"Facture {invoice_number} — {company_name}",
            show_date=True,
        ),
        elements=elements,
        metadata={
            "filename": f"facture_{invoice_number}.pdf",
            "type": "invoice",
        },
    )
