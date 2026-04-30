import io
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable,
)
from reportlab.lib.enums import TA_CENTER

PAGE_W, PAGE_H = A4
MARGIN = 20 * mm

PRIMARY = colors.HexColor("#1976D2")
LIGHT_BG = colors.HexColor("#E3F2FD")
DARK_TEXT = colors.HexColor("#212121")
MUTED = colors.HexColor("#757575")
WHITE = colors.white


def _styles():
    base = getSampleStyleSheet()
    return {
        "school": ParagraphStyle(
            "school",
            fontSize=22,
            textColor=WHITE,
            alignment=TA_CENTER,
            fontName="Helvetica-Bold",
            spaceAfter=2,
        ),
        "report_title": ParagraphStyle(
            "report_title",
            fontSize=11,
            textColor=colors.HexColor("#BBDEFB"),
            alignment=TA_CENTER,
            fontName="Helvetica",
        ),
        "section_header": ParagraphStyle(
            "section_header",
            fontSize=10,
            textColor=WHITE,
            fontName="Helvetica-Bold",
            leftIndent=6,
            spaceAfter=0,
            spaceBefore=0,
        ),
        "label": ParagraphStyle(
            "label",
            fontSize=9,
            textColor=MUTED,
            fontName="Helvetica",
        ),
        "value": ParagraphStyle(
            "value",
            fontSize=10,
            textColor=DARK_TEXT,
            fontName="Helvetica",
        ),
        "footer": ParagraphStyle(
            "footer",
            fontSize=8,
            textColor=MUTED,
            alignment=TA_CENTER,
        ),
    }


def _fmt(val, fallback="—"):
    if val is None or val == "":
        return fallback
    if isinstance(val, bool):
        return "Active" if val else "Inactive"
    return str(val)


def _fmt_date(val):
    if not val:
        return "—"
    try:
        dt = datetime.fromisoformat(str(val).replace("Z", "+00:00"))
        return dt.strftime("%d %b %Y")
    except Exception:
        return str(val)


def _section_table(rows: list[tuple[str, str]], styles: dict) -> Table:
    data = [[Paragraph(label, styles["label"]), Paragraph(value, styles["value"])] for label, value in rows]
    t = Table(data, colWidths=[55 * mm, 95 * mm])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [WHITE, colors.HexColor("#F5F5F5")]),
    ]))
    return t


def _section_header(title: str, styles: dict):
    data = [[Paragraph(title, styles["section_header"])]]
    t = Table(data, colWidths=[PAGE_W - 2 * MARGIN])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), PRIMARY),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
    ]))
    return t


def generate_pdf(student: dict) -> bytes:
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=MARGIN,
        bottomMargin=MARGIN,
    )
    styles = _styles()
    story = []

    header_data = [[
        Paragraph("School Management System", styles["school"]),
    ], [
        Paragraph("Student Academic Report", styles["report_title"]),
    ]]
    header_table = Table(header_data, colWidths=[PAGE_W - 2 * MARGIN])
    header_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), PRIMARY),
        ("TOPPADDING", (0, 0), (0, 0), 14),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 6 * mm))

    meta_data = [
        [
            Paragraph("Student ID", styles["label"]),
            Paragraph(_fmt(student.get("id")), styles["value"]),
            Paragraph("Generated On", styles["label"]),
            Paragraph(datetime.now().strftime("%d %b %Y, %H:%M"), styles["value"]),
        ],
        [
            Paragraph("System Access", styles["label"]),
            Paragraph(_fmt(student.get("systemAccess")), styles["value"]),
            Paragraph("Admission Date", styles["label"]),
            Paragraph(_fmt_date(student.get("admissionDate")), styles["value"]),
        ],
    ]
    meta_table = Table(meta_data, colWidths=[40 * mm, 55 * mm, 40 * mm, 35 * mm])
    meta_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), LIGHT_BG),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 5 * mm))

    story.append(_section_header("Personal Information", styles))
    story.append(_section_table([
        ("Full Name", _fmt(student.get("name"))),
        ("Email", _fmt(student.get("email"))),
        ("Gender", _fmt(student.get("gender"))),
        ("Date of Birth", _fmt_date(student.get("dob"))),
        ("Phone", _fmt(student.get("phone"))),
    ], styles))
    story.append(Spacer(1, 4 * mm))

    story.append(_section_header("Academic Information", styles))
    story.append(_section_table([
        ("Class", _fmt(student.get("class"))),
        ("Section", _fmt(student.get("section"))),
        ("Roll Number", _fmt(student.get("roll"))),
        ("Class Teacher", _fmt(student.get("reporterName"))),
    ], styles))
    story.append(Spacer(1, 4 * mm))

    story.append(_section_header("Family & Guardian Information", styles))
    story.append(_section_table([
        ("Father's Name", _fmt(student.get("fatherName"))),
        ("Father's Phone", _fmt(student.get("fatherPhone"))),
        ("Mother's Name", _fmt(student.get("motherName"))),
        ("Mother's Phone", _fmt(student.get("motherPhone"))),
        ("Guardian's Name", _fmt(student.get("guardianName"))),
        ("Guardian's Phone", _fmt(student.get("guardianPhone"))),
        ("Relation of Guardian", _fmt(student.get("relationOfGuardian"))),
    ], styles))
    story.append(Spacer(1, 4 * mm))

    story.append(_section_header("Address Information", styles))
    story.append(_section_table([
        ("Current Address", _fmt(student.get("currentAddress"))),
        ("Permanent Address", _fmt(student.get("permanentAddress"))),
    ], styles))
    story.append(Spacer(1, 8 * mm))

    story.append(HRFlowable(width="100%", thickness=0.5, color=MUTED))
    story.append(Spacer(1, 3 * mm))
    story.append(Paragraph(
        f"This report was automatically generated on {datetime.now().strftime('%d %b %Y at %H:%M')}. "
        "For official use only.",
        styles["footer"],
    ))

    doc.build(story)
    return buffer.getvalue()
