"""
GK GROCERY STORE – PDF Invoice Generation Utility
Generates clean, professional commercial receipts and invoices using ReportLab.
"""

import io
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT

from config import APP_NAME, APP_SUBTITLE, APP_TAGLINE


def generate_invoice_pdf(sale_data: dict, items: list[dict]) -> io.BytesIO:
    """
    Generates a beautifully styled PDF invoice in-memory.
    sale_data: dict containing invoice_no, customer_name, customer_phone,
               sale_date, total_amount, discount_amount, grand_total, payment_method.
    items: list of dicts with product_name, category, unit, quantity, selling_price, subtotal.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    story = []
    styles = getSampleStyleSheet()

    # Custom typography styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor("#14532D"),
        alignment=TA_CENTER
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=13,
        textColor=colors.HexColor("#475569"),
        alignment=TA_CENTER
    )

    tagline_style = ParagraphStyle(
        'DocTagline',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9,
        leading=11,
        textColor=colors.HexColor("#22C55E"),
        alignment=TA_CENTER
    )

    section_heading = ParagraphStyle(
        'SectionHeading',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=colors.HexColor("#1E293B")
    )

    body_style = ParagraphStyle(
        'DocBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#334155")
    )

    right_bold = ParagraphStyle(
        'RightBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        alignment=TA_RIGHT,
        textColor=colors.HexColor("#1E293B")
    )

    right_text = ParagraphStyle(
        'RightText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12,
        alignment=TA_RIGHT,
        textColor=colors.HexColor("#334155")
    )

    footer_style = ParagraphStyle(
        'FooterText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#64748B")
    )

    # 1. Header & Store Branding
    from config import ASSETS_DIR
    logo_file = ASSETS_DIR / "logo.png"
    if logo_file.exists():
        try:
            from reportlab.platypus import Image as RLImage
            logo_img = RLImage(str(logo_file), width=50, height=50)
            logo_img.hAlign = 'CENTER'
            story.append(logo_img)
            story.append(Spacer(1, 4))
        except Exception:
            pass

    story.append(Paragraph(f"<b>{APP_NAME}</b>", title_style))
    story.append(Spacer(1, 2))
    story.append(Paragraph(APP_SUBTITLE, subtitle_style))
    story.append(Paragraph(f'"{APP_TAGLINE}"', tagline_style))
    story.append(Spacer(1, 4))
    story.append(Paragraph("Shop No. 12, Main Market Road, Near City Center, Pune - 411001 | Phone: +91 8010434421", subtitle_style))
    story.append(Spacer(1, 10))

    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#14532D"), spaceBefore=4, spaceAfter=12))

    # 2. Invoice Meta & Customer Details
    sale_date_str = str(sale_data.get('sale_date', datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    
    meta_data = [
        [
            Paragraph("<b>BILLED TO:</b>", section_heading),
            Paragraph("<b>INVOICE DETAILS:</b>", section_heading)
        ],
        [
            Paragraph(f"<b>Customer:</b> {sale_data.get('customer_name', 'Walk-in Customer')}", body_style),
            Paragraph(f"<b>Invoice No:</b> <font color='#14532D'><b>{sale_data.get('invoice_no', 'N/A')}</b></font>", body_style)
        ],
        [
            Paragraph(f"<b>Contact:</b> {sale_data.get('customer_phone', 'N/A')}", body_style),
            Paragraph(f"<b>Date & Time:</b> {sale_date_str}", body_style)
        ],
        [
            Paragraph("<b>GSTIN / Store Reg:</b> 27AAAPL1234F1Z5", body_style),
            Paragraph(f"<b>Payment Mode:</b> {sale_data.get('payment_method', 'Cash')} (PAID)", body_style)
        ]
    ]

    meta_table = Table(meta_data, colWidths=[270, 250])
    meta_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 15))

    # 3. Itemized Products Table
    headers = ["#", "Item Description", "Category", "Rate (Rs)", "Qty", "Amount (Rs)"]
    table_rows = [headers]

    for idx, it in enumerate(items, 1):
        item_name = it.get('product_name', 'Item')
        unit = it.get('unit', '')
        qty = float(it.get('quantity', 1))
        rate = float(it.get('selling_price', 0))
        subtotal = float(it.get('subtotal', rate * qty))
        cat = it.get('category', 'Grocery')

        unit_lower = str(unit or '').lower().strip()
        if unit_lower in ['kg', 'kilogram']:
            if qty < 1.0:
                qty_display = f"{qty * 1000:g} g ({qty:g} kg)"
            elif (qty * 1000) % 1000 != 0:
                qty_display = f"{qty:g} kg ({qty * 1000:g} g)"
            else:
                qty_display = f"{qty:g} kg"
        elif unit_lower in ['litre', 'liter']:
            if qty < 1.0:
                qty_display = f"{qty * 1000:g} ml ({qty:g} L)"
            elif (qty * 1000) % 1000 != 0:
                qty_display = f"{qty:g} L ({qty * 1000:g} ml)"
            else:
                qty_display = f"{qty:g} L"
        else:
            qty_display = f"{qty:g} {unit}".strip()

        table_rows.append([
            str(idx),
            Paragraph(item_name, body_style),
            Paragraph(cat, body_style),
            f"{rate:,.2f}",
            qty_display,
            f"{subtotal:,.2f}"
        ])

    items_table = Table(
        table_rows,
        colWidths=[25, 175, 95, 65, 85, 78]
    )

    items_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#14532D")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('ALIGN', (0, 0), (0, -1), 'CENTER'),
        ('ALIGN', (1, 0), (2, -1), 'LEFT'),
        ('ALIGN', (3, 0), (3, -1), 'RIGHT'),
        ('ALIGN', (4, 0), (4, -1), 'CENTER'),
        ('ALIGN', (5, 0), (5, -1), 'RIGHT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
    ]))

    story.append(items_table)
    story.append(Spacer(1, 12))

    # 4. Financial Totals & Summary Table
    total_amount = float(sale_data.get('total_amount', 0))
    discount = float(sale_data.get('discount_amount', 0))
    grand_total = float(sale_data.get('grand_total', total_amount - discount))

    summary_data = [
        [Paragraph("", body_style), Paragraph("Items Subtotal:", right_text), Paragraph(f"Rs. {total_amount:,.2f}", right_bold)],
        [Paragraph("", body_style), Paragraph("Discount Applied:", right_text), Paragraph(f"- Rs. {discount:,.2f}", right_bold)],
        [Paragraph("", body_style), Paragraph("<b>Grand Total:</b>", right_bold), Paragraph(f"<b>Rs. {grand_total:,.2f}</b>", right_bold)],
    ]

    summary_table = Table(summary_data, colWidths=[270, 125, 128])
    summary_table.setStyle(TableStyle([
        ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
        ('LINEABOVE', (1, 2), (2, 2), 1, colors.HexColor("#14532D")),
        ('LINEBELOW', (1, 2), (2, 2), 1.5, colors.HexColor("#14532D")),
        ('BACKGROUND', (1, 2), (2, 2), colors.HexColor("#DCFCE7")),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))

    story.append(summary_table)
    story.append(Spacer(1, 25))

    # 5. Thank You & Terms
    story.append(HRFlowable(width="100%", thickness=0.8, color=colors.HexColor("#CBD5E1"), spaceBefore=4, spaceAfter=8))
    story.append(Paragraph("<b>Thank you for shopping with GK Grocery Store!</b>", ParagraphStyle(
        'ThankYou',
        parent=footer_style,
        fontName='Helvetica-Bold',
        fontSize=11,
        textColor=colors.HexColor("#14532D")
    )))
    story.append(Spacer(1, 3))
    story.append(Paragraph("For support or inquiries, please contact info@gkgrocery.com | +91 8010434421", footer_style))
    story.append(Paragraph("Goods once sold can be exchanged within 24 hours with this original tax invoice.", footer_style))

    # Build document
    doc.build(story)
    buffer.seek(0)
    return buffer

