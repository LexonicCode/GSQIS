#!/usr/bin/env python3
"""
Generate branded PDFs for the GSQIS ArcGIS Pro Toolbox distribution.

Idox Geospatial branding:
  Primary blue : #003A70  (deep navy)
  Accent teal  : #00A9A5
  Light grey   : #F5F5F5
  Body text    : #222222
  Font         : Helvetica (built-in PDF font, approximating a clean sans-serif)
"""

import os
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    HRFlowable,
    NextPageTemplate,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.platypus.tableofcontents import TableOfContents


# ---------------------------------------------------------------------------
# Brand colours
# ---------------------------------------------------------------------------
BRAND_NAVY   = colors.HexColor("#003A70")
BRAND_TEAL   = colors.HexColor("#00A9A5")
BRAND_ORANGE = colors.HexColor("#E8580A")   # accent for caution/tip boxes
BRAND_LGREY  = colors.HexColor("#F5F5F5")
BRAND_DGREY  = colors.HexColor("#4A4A4A")
BRAND_BLACK  = colors.HexColor("#222222")
BRAND_WHITE  = colors.white


# ---------------------------------------------------------------------------
# Styles
# ---------------------------------------------------------------------------
def build_styles():
    styles = getSampleStyleSheet()

    # Cover title
    styles.add(ParagraphStyle(
        "CoverTitle",
        fontName="Helvetica-Bold",
        fontSize=28,
        leading=34,
        textColor=BRAND_WHITE,
        alignment=TA_LEFT,
        spaceAfter=6,
    ))

    # Cover subtitle
    styles.add(ParagraphStyle(
        "CoverSubtitle",
        fontName="Helvetica",
        fontSize=16,
        leading=20,
        textColor=BRAND_WHITE,
        alignment=TA_LEFT,
        spaceAfter=4,
    ))

    # Cover meta (version, contact)
    styles.add(ParagraphStyle(
        "CoverMeta",
        fontName="Helvetica",
        fontSize=10,
        leading=14,
        textColor=BRAND_WHITE,
        alignment=TA_LEFT,
    ))

    # Section heading
    styles.add(ParagraphStyle(
        "IdoxSectionHeading",
        fontName="Helvetica-Bold",
        fontSize=15,
        leading=20,
        textColor=BRAND_NAVY,
        spaceBefore=18,
        spaceAfter=6,
    ))

    # Sub-heading
    styles.add(ParagraphStyle(
        "IdoxSubHeading",
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=15,
        textColor=BRAND_NAVY,
        spaceBefore=12,
        spaceAfter=4,
    ))

    # Body text
    styles.add(ParagraphStyle(
        "IdoxBody",
        fontName="Helvetica",
        fontSize=10,
        leading=15,
        textColor=BRAND_BLACK,
        spaceAfter=6,
    ))

    # Bullet
    styles.add(ParagraphStyle(
        "IdoxBullet",
        fontName="Helvetica",
        fontSize=10,
        leading=15,
        textColor=BRAND_BLACK,
        leftIndent=18,
        spaceAfter=4,
        bulletIndent=6,
    ))

    # Code / monospace
    styles.add(ParagraphStyle(
        "IdoxCode",
        fontName="Courier",
        fontSize=9,
        leading=13,
        textColor=BRAND_DGREY,
        backColor=BRAND_LGREY,
        leftIndent=12,
        rightIndent=12,
        spaceBefore=4,
        spaceAfter=4,
        borderPadding=6,
    ))

    # Note / tip box
    styles.add(ParagraphStyle(
        "IdoxNote",
        fontName="Helvetica-Oblique",
        fontSize=9.5,
        leading=14,
        textColor=BRAND_DGREY,
        leftIndent=12,
        rightIndent=12,
        spaceBefore=4,
        spaceAfter=4,
    ))

    # Footer
    styles.add(ParagraphStyle(
        "IdoxFooter",
        fontName="Helvetica",
        fontSize=8,
        leading=10,
        textColor=BRAND_DGREY,
        alignment=TA_CENTER,
    ))

    # Table header cell
    styles.add(ParagraphStyle(
        "IdoxTableHeader",
        fontName="Helvetica-Bold",
        fontSize=9.5,
        leading=13,
        textColor=BRAND_WHITE,
    ))

    # Table body cell
    styles.add(ParagraphStyle(
        "IdoxTableBody",
        fontName="Helvetica",
        fontSize=9.5,
        leading=13,
        textColor=BRAND_BLACK,
    ))

    return styles


# ---------------------------------------------------------------------------
# Page templates
# ---------------------------------------------------------------------------
PAGE_W, PAGE_H = A4
MARGIN = 2 * cm
CONTENT_W = PAGE_W - 2 * MARGIN


def _draw_cover_bg(canvas, doc):
    canvas.saveState()
    # Full-page navy background
    canvas.setFillColor(BRAND_NAVY)
    canvas.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    # Teal accent strip at bottom
    canvas.setFillColor(BRAND_TEAL)
    canvas.rect(0, 0, PAGE_W, 1.2 * cm, fill=1, stroke=0)
    canvas.restoreState()


def _draw_page_header_footer(canvas, doc):
    canvas.saveState()
    # Header bar
    canvas.setFillColor(BRAND_NAVY)
    canvas.rect(0, PAGE_H - 1.4 * cm, PAGE_W, 1.4 * cm, fill=1, stroke=0)
    # Header text — product name (left)
    canvas.setFont("Helvetica-Bold", 9)
    canvas.setFillColor(BRAND_WHITE)
    canvas.drawString(MARGIN, PAGE_H - 0.9 * cm, "Idox Geospatial  |  GSQIS Toolbox for ArcGIS Pro")
    # Header text — doc title (right)
    canvas.setFont("Helvetica", 9)
    canvas.drawRightString(PAGE_W - MARGIN, PAGE_H - 0.9 * cm, doc.title)

    # Footer rule
    canvas.setStrokeColor(BRAND_TEAL)
    canvas.setLineWidth(1.5)
    canvas.line(MARGIN, 1.4 * cm, PAGE_W - MARGIN, 1.4 * cm)
    # Footer text — left
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(BRAND_DGREY)
    canvas.drawString(MARGIN, 0.8 * cm, "© Idox Geospatial  |  geo-customersupport@idoxgroup.com")
    # Footer text — page number (right)
    canvas.drawRightString(PAGE_W - MARGIN, 0.8 * cm, f"Page {doc.page}")
    canvas.restoreState()


def build_doc_template(output_path, doc_title):
    doc = BaseDocTemplate(
        output_path,
        pagesize=A4,
        title=doc_title,
        author="Idox Geospatial",
        subject=doc_title,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=MARGIN + 1.4 * cm,   # below header bar
        bottomMargin=MARGIN + 1.0 * cm,
    )
    doc.title = doc_title  # stored for header callback

    # Cover page template (no header/footer — full-bleed navy)
    cover_frame = Frame(
        MARGIN, 4 * cm,
        PAGE_W - 2 * MARGIN, PAGE_H - 8 * cm,
        id="cover",
    )
    cover_tpl = PageTemplate(
        id="Cover",
        frames=[cover_frame],
        onPage=_draw_cover_bg,
    )

    # Normal page template
    content_frame = Frame(
        MARGIN,
        MARGIN + 1.4 * cm,
        CONTENT_W,
        PAGE_H - 2 * MARGIN - 1.4 * cm - 1.0 * cm,
        id="content",
    )
    normal_tpl = PageTemplate(
        id="Normal",
        frames=[content_frame],
        onPage=_draw_page_header_footer,
    )

    doc.addPageTemplates([cover_tpl, normal_tpl])
    return doc


# ---------------------------------------------------------------------------
# Reusable flowable helpers
# ---------------------------------------------------------------------------
def heading(text, styles):
    return Paragraph(text, styles["IdoxSectionHeading"])


def subheading(text, styles):
    return Paragraph(text, styles["IdoxSubHeading"])


def body(text, styles):
    return Paragraph(text, styles["IdoxBody"])


def bullet(text, styles):
    return Paragraph(f"• {text}", styles["IdoxBullet"])


def code(text, styles):
    # Escape any XML entities in code blocks
    safe = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return Paragraph(safe, styles["IdoxCode"])


def note(text, styles):
    return Paragraph(f"<i>ℹ {text}</i>", styles["IdoxNote"])


def tip(text, styles):
    return Paragraph(f"<i>💡 Tip: {text}</i>", styles["IdoxNote"])


def hrule():
    return HRFlowable(
        width="100%",
        thickness=0.8,
        color=BRAND_TEAL,
        spaceAfter=6,
        spaceBefore=6,
    )


def simple_table(headers, rows, styles, col_widths=None):
    """Build a styled two-column-or-more table."""
    header_cells = [Paragraph(h, styles["IdoxTableHeader"]) for h in headers]
    data = [header_cells]
    for row in rows:
        data.append([Paragraph(str(c), styles["IdoxTableBody"]) for c in row])

    if col_widths is None:
        n = len(headers)
        col_widths = [CONTENT_W / n] * n

    tbl = Table(data, colWidths=col_widths, repeatRows=1)
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), BRAND_NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), BRAND_WHITE),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [BRAND_WHITE, BRAND_LGREY]),
        ("GRID", (0, 0), (-1, -1), 0.4, BRAND_TEAL),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    return tbl


def checklist_table(items, styles):
    """Render a checklist as a table with checkboxes."""
    data = [[Paragraph("☐", styles["IdoxTableBody"]), Paragraph(item, styles["IdoxTableBody"])] for item in items]
    tbl = Table(data, colWidths=[0.8 * cm, CONTENT_W - 0.8 * cm])
    tbl.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [BRAND_WHITE, BRAND_LGREY]),
    ]))
    return tbl


def cover_block(title_lines, subtitle, meta_lines, styles):
    """Return flowables for the cover page."""
    items = []
    for line in title_lines:
        items.append(Paragraph(line, styles["CoverTitle"]))
    items.append(Spacer(1, 0.4 * cm))
    items.append(Paragraph(subtitle, styles["CoverSubtitle"]))
    items.append(Spacer(1, 1.5 * cm))
    for line in meta_lines:
        items.append(Paragraph(line, styles["CoverMeta"]))
    return items


# ---------------------------------------------------------------------------
# Document 1 — Installation & Testing Guide
# ---------------------------------------------------------------------------
def build_installation_guide(output_path):
    styles = build_styles()
    doc = build_doc_template(output_path, "Installation & Testing Guide")
    story = []

    # ---- Cover ----
    story += cover_block(
        title_lines=["GSQIS Toolbox", "for ArcGIS Pro"],
        subtitle="Installation & Testing Guide",
        meta_lines=[
            "Version 1.0  |  ArcGIS Pro 3.0+",
            " ",
            "Support: geo-customersupport@idoxgroup.com",
            "SDK:  https://sdk.idoxgeospatial.co.uk/",
            " ",
            "© Idox Geospatial",
        ],
        styles=styles,
    )
    story.append(NextPageTemplate("Normal"))
    story.append(PageBreak())

    # ---- Section 1: Prerequisites ----
    story.append(heading("1.  Before You Start — Prerequisites", styles))
    story.append(hrule())
    story.append(body(
        "Before installing the GSQIS Toolbox, please confirm the following requirements are met:",
        styles,
    ))
    story.append(simple_table(
        headers=["Requirement", "Details"],
        rows=[
            ["ArcGIS Pro", "Version 3.0 or later"],
            ["Operating System", "Windows 10 or Windows 11 (64-bit)"],
            ["User Permissions", "Ability to add files and toolboxes within ArcGIS Pro"],
            ["Disk Space", "At least 5 MB free"],
        ],
        styles=styles,
        col_widths=[5 * cm, CONTENT_W - 5 * cm],
    ))
    story.append(Spacer(1, 0.3 * cm))
    story.append(note("No internet connection or additional software is required to use the toolbox.", styles))
    story.append(Spacer(1, 0.4 * cm))

    story.append(subheading("How to Check Your ArcGIS Pro Version", styles))
    for step in [
        "Open <b>ArcGIS Pro</b>.",
        "Click the <b>Project</b> tab in the top-left ribbon.",
        "Select <b>About ArcGIS Pro</b> at the bottom of the left panel.",
        "Your version number is shown at the top (e.g., <i>ArcGIS Pro 3.2.0</i>).",
    ]:
        story.append(bullet(step, styles))
    story.append(Spacer(1, 0.3 * cm))
    story.append(note(
        "If your version is below 3.0, contact your GIS administrator or Esri support to upgrade.",
        styles,
    ))

    # ---- Section 2: What's in the package ----
    story.append(heading("2.  What's in the Package", styles))
    story.append(hrule())
    story.append(body("The distribution ZIP file contains the following files:", styles))
    story.append(simple_table(
        headers=["File", "Description"],
        rows=[
            ["GSQIS_Toolbox.pyt", "The ArcGIS Pro toolbox file — required for installation"],
            ["Installation_and_Testing_Guide.md", "This guide in Markdown format"],
            ["Installation_and_Testing_Guide.pdf", "This guide in PDF format"],
            ["FAQ_and_Troubleshooting.md", "Frequently asked questions (Markdown)"],
            ["FAQ_and_Troubleshooting.pdf", "Frequently asked questions (PDF)"],
        ],
        styles=styles,
        col_widths=[7 * cm, CONTENT_W - 7 * cm],
    ))

    # ---- Section 3: Installation ----
    story.append(heading("3.  Installation", styles))
    story.append(hrule())

    story.append(subheading("Step 1 — Unzip the Package", styles))
    for step in [
        "Right-click <b>GSQIS-ArcGIS-Toolbox-v1.0.zip</b> in Windows File Explorer.",
        "Select <b>Extract All…</b>",
        "Choose a convenient folder (e.g., <font name='Courier' size=9>C:\\GIS\\Tools\\GSQIS\\</font>) and click <b>Extract</b>.",
        "Make a note of the folder path — you will need it in Step 3.",
    ]:
        story.append(bullet(step, styles))
    story.append(tip(
        "Avoid extracting to a network drive or a system folder. "
        "Your Documents folder or a dedicated GIS tools folder works best.",
        styles,
    ))
    story.append(Spacer(1, 0.2 * cm))

    story.append(subheading("Step 2 — Open ArcGIS Pro", styles))
    story.append(body(
        "Open ArcGIS Pro and either open an existing project or create a new one.",
        styles,
    ))
    story.append(tip(
        "From the splash screen, choose <b>Map</b> under <i>New Project</i> to create a blank project.",
        styles,
    ))
    story.append(Spacer(1, 0.2 * cm))

    story.append(subheading("Step 3 — Add the Toolbox to Your Project", styles))
    for step in [
        "In the <b>Catalog</b> pane on the right side of the screen, locate the <b>Toolboxes</b> section. "
        "(If the Catalog pane is not visible: click <b>View</b> in the top ribbon → <b>Catalog Pane</b>.)",
        "Right-click <b>Toolboxes</b> and choose <b>Add Toolbox</b>.",
        "In the file browser, navigate to the folder where you extracted the ZIP file.",
        "Select <b>GSQIS_Toolbox.pyt</b> and click <b>OK</b>.",
        "The toolbox now appears under <b>Toolboxes</b> in the Catalog pane, labelled <b>GSQIS Toolbox</b>.",
    ]:
        story.append(bullet(step, styles))
    story.append(Spacer(1, 0.2 * cm))

    story.append(subheading("Step 4 — Confirm the Toolbox is Listed", styles))
    story.append(body("After adding the toolbox, you should see the following in the Catalog pane:", styles))
    story.append(code(
        "Toolboxes\n"
        "└── GSQIS Toolbox\n"
        "    └── Analysis\n"
        "        └── Layer Statistics",
        styles,
    ))
    story.append(body("If <b>Layer Statistics</b> is visible under <b>Analysis</b>, installation is complete.", styles))

    # ---- Section 4: Running First Analysis ----
    story.append(heading("4.  Running Your First Analysis", styles))
    story.append(hrule())
    story.append(body(
        "The <b>Layer Statistics</b> tool computes a summary of all data fields in any feature layer "
        "and saves the results to a text report. Follow these steps:",
        styles,
    ))

    story.append(subheading("Step 1 — Load a Layer", styles))
    for step in [
        "In the <b>Catalog</b> pane, browse to any shapefile or feature class.",
        "Right-click it and choose <b>Add To Current Map</b>.",
    ]:
        story.append(bullet(step, styles))

    story.append(subheading("Step 2 — Open the Layer Statistics Tool", styles))
    for step in [
        "In the Catalog pane, expand <b>Toolboxes → GSQIS Toolbox → Analysis</b>.",
        "Double-click <b>Layer Statistics</b>.",
        "The tool dialog opens in the <b>Geoprocessing</b> pane.",
    ]:
        story.append(bullet(step, styles))

    story.append(subheading("Step 3 — Set Parameters and Run", styles))
    story.append(simple_table(
        headers=["Parameter", "What to enter"],
        rows=[
            ["Input Feature Layer", "Select your loaded layer from the dropdown"],
            ["Output Report File", "Click the folder icon and choose where to save (e.g., C:\\GIS\\Output\\stats.txt)"],
            ["Maximum Unique Values to Report", "Leave as 20 (default) unless you want to change the number of text values listed"],
        ],
        styles=styles,
        col_widths=[6 * cm, CONTENT_W - 6 * cm],
    ))
    story.append(Spacer(1, 0.2 * cm))
    story.append(body(
        "Click <b>Run</b> (the blue button at the bottom of the Geoprocessing pane). "
        "When the tool finishes, you will see a message such as:",
        styles,
    ))
    story.append(code("Report written to: C:\\GIS\\Output\\stats.txt", styles))
    story.append(body("Open the output <b>.txt</b> file in Notepad to review your layer statistics.", styles))

    # ---- Section 5: Verification ----
    story.append(heading("5.  Verifying Successful Installation", styles))
    story.append(hrule())
    story.append(body("Use the checklist below to confirm everything is working correctly:", styles))
    story.append(checklist_table([
        "<b>GSQIS Toolbox</b> appears under Toolboxes in the Catalog pane.",
        "<b>Layer Statistics</b> tool opens when double-clicked.",
        "The tool runs without errors on a test layer.",
        "An output .txt report file is created at the path you specified.",
        "The report contains a LAYER SUMMARY section and a FIELD STATISTICS section.",
    ], styles))

    # ---- Section 6: Uninstalling ----
    story.append(heading("6.  Uninstalling the Toolbox", styles))
    story.append(hrule())
    for step in [
        "In the <b>Catalog</b> pane, right-click <b>GSQIS Toolbox</b> under Toolboxes.",
        "Select <b>Remove</b>.",
    ]:
        story.append(bullet(step, styles))
    story.append(Spacer(1, 0.2 * cm))
    story.append(note(
        "Removing the toolbox only removes it from the current project. "
        "To fully remove it from your computer, delete the folder containing GSQIS_Toolbox.pyt. "
        "Output reports you have already generated are not affected.",
        styles,
    ))

    # ---- Section 7: Help ----
    story.append(heading("7.  Getting Help", styles))
    story.append(hrule())
    story.append(simple_table(
        headers=["Channel", "Details"],
        rows=[
            ["Email support", "geo-customersupport@idoxgroup.com"],
            ["SDK & documentation", "https://sdk.idoxgeospatial.co.uk/"],
        ],
        styles=styles,
        col_widths=[5 * cm, CONTENT_W - 5 * cm],
    ))
    story.append(Spacer(1, 0.3 * cm))
    story.append(body("When contacting support, please include:", styles))
    for item in [
        "Your ArcGIS Pro version number",
        "A description of the issue or error message",
        "The name of the layer you were working with (if applicable)",
    ]:
        story.append(bullet(item, styles))

    doc.build(story)
    print(f"Created: {output_path}")


# ---------------------------------------------------------------------------
# Document 2 — FAQ & Troubleshooting Guide
# ---------------------------------------------------------------------------
def build_faq_guide(output_path):
    styles = build_styles()
    doc = build_doc_template(output_path, "FAQ & Troubleshooting Guide")
    story = []

    # ---- Cover ----
    story += cover_block(
        title_lines=["GSQIS Toolbox", "for ArcGIS Pro"],
        subtitle="FAQ & Troubleshooting Guide",
        meta_lines=[
            "Version 1.0  |  ArcGIS Pro 3.0+",
            " ",
            "Support: geo-customersupport@idoxgroup.com",
            "SDK:  https://sdk.idoxgeospatial.co.uk/",
            " ",
            "© Idox Geospatial",
        ],
        styles=styles,
    )
    story.append(NextPageTemplate("Normal"))
    story.append(PageBreak())

    # ---- FAQ ----
    story.append(heading("Frequently Asked Questions", styles))
    story.append(hrule())

    faq_items = [
        (
            "What is the GSQIS Toolbox?",
            "The GSQIS Toolbox is an ArcGIS Pro plugin (Python Toolbox) developed by Idox Geospatial. "
            "It provides geospatial analysis tools — starting with the <b>Layer Statistics</b> tool, "
            "which summarises the data in any feature layer and exports a readable report.",
        ),
        (
            "Which versions of ArcGIS Pro does the toolbox support?",
            "The GSQIS Toolbox is supported on <b>ArcGIS Pro 3.0 and above</b> running on "
            "Windows 10 or Windows 11 (64-bit).",
        ),
        (
            "Do I need administrator rights to install the toolbox?",
            "No. Extract the toolbox files to a folder you own (e.g., your Documents folder or a "
            "dedicated GIS tools folder). Avoid placing files in "
            "<font name='Courier' size=9>C:\\Program Files\\</font> or other protected directories.",
        ),
        (
            "Does the toolbox require an internet connection?",
            "No. The toolbox works entirely offline after installation.",
        ),
        (
            "Do I need to install any additional Python packages?",
            "No. The toolbox uses only <b>arcpy</b>, which is built into ArcGIS Pro. "
            "No extra Python libraries are required.",
        ),
        (
            "Can I use the toolbox with ArcGIS Desktop (ArcMap)?",
            "No. The GSQIS Toolbox is designed specifically for <b>ArcGIS Pro 3.0+</b> and is not "
            "compatible with ArcGIS Desktop (ArcMap).",
        ),
        (
            "Will the toolbox modify my existing data?",
            "No. The toolbox only reads your data to compute statistics. It never modifies source layers. "
            "The only output it creates is the text report file you specify.",
        ),
        (
            "Can I add the toolbox to multiple ArcGIS Pro projects?",
            "Yes. You can add the same <font name='Courier' size=9>GSQIS_Toolbox.pyt</font> file to as "
            "many ArcGIS Pro projects as you like by following the installation steps in each project.",
        ),
        (
            "What types of data does Layer Statistics support?",
            "The Layer Statistics tool works with any <b>vector feature layer</b> — points, lines, or "
            "polygons — including shapefiles, file geodatabase feature classes, enterprise geodatabase "
            "layers, and in-memory layers.",
        ),
        (
            "What does the output report contain?",
            "The output is a plain-text (.txt) file with two sections: (1) <b>LAYER SUMMARY</b> — "
            "name, coordinate system, geometry type, feature count, field count; and "
            "(2) <b>FIELD STATISTICS</b> — numeric fields yield count, min, max, mean, median, sum, "
            "and standard deviation; text/categorical fields yield count, empty count, unique values, "
            "and the most frequently occurring values.",
        ),
    ]

    for q, a in faq_items:
        story.append(subheading(q, styles))
        story.append(body(a, styles))
        story.append(Spacer(1, 0.15 * cm))

    # ---- Troubleshooting ----
    story.append(heading("Troubleshooting", styles))
    story.append(hrule())

    trouble_items = [
        (
            "Toolbox does not appear in the Catalog pane after adding it",
            [
                "<b>Wrong file selected.</b> Make sure you selected "
                "<font name='Courier' size=9>GSQIS_Toolbox.pyt</font> (not a folder or other file).",
                "<b>Catalog pane needs refreshing.</b> Right-click <b>Toolboxes</b> → <b>Refresh</b>.",
                "<b>Wrong project open.</b> Check that the correct project is currently active.",
            ],
        ),
        (
            "ERROR 000732: Input Features: Dataset does not exist or is not supported",
            [
                "The selected layer is not a valid vector feature layer. "
                "Ensure you have loaded a vector layer (shapefile or feature class) into your map.",
            ],
        ),
        (
            "ERROR 000210: Cannot create output …",
            [
                "The output report file path is not writable.",
                "Try saving the output to a folder you own, such as "
                "<font name='Courier' size=9>C:\\Users\\YourName\\Documents\\</font>.",
                "Avoid paths on read-only network drives.",
            ],
        ),
        (
            "ExecuteError: Failed to execute (LayerStatistics)",
            [
                "Restart ArcGIS Pro and re-run the tool.",
                "Ensure the input layer is fully loaded (visible on the map with features).",
                "If the error persists, contact support with the full error text from the <b>Messages</b> panel.",
            ],
        ),
        (
            "Output report is empty or shows no field statistics",
            [
                "The input layer may contain no features. Open the attribute table to check.",
                "If the layer has features but no attribute fields (other than geometry), "
                "only layer-level information will appear.",
            ],
        ),
        (
            "ArcGIS Pro is slow to run the analysis",
            [
                "Performance depends on dataset size. Layers with millions of features may take several minutes.",
                "Test first with a smaller subset: right-click the layer → <b>Data → Export Features</b>.",
            ],
        ),
        (
            "Toolbox disappears after closing and reopening ArcGIS Pro",
            [
                "Toolboxes added manually are saved to the current project (.aprx file). "
                "If you opened a different project, re-add the toolbox.",
                "To avoid this in future, save your project after adding the toolbox (<b>Ctrl+S</b>).",
            ],
        ),
        (
            "Yellow warning triangle next to the toolbox",
            [
                "The .pyt file has been moved or deleted from its original location.",
                "Re-add the toolbox: right-click <b>Toolboxes → Add Toolbox</b> and browse to "
                "the current location of <font name='Courier' size=9>GSQIS_Toolbox.pyt</font>.",
            ],
        ),
    ]

    for title, bullets in trouble_items:
        story.append(subheading(title, styles))
        for b_text in bullets:
            story.append(bullet(b_text, styles))
        story.append(Spacer(1, 0.2 * cm))

    # ---- Contact ----
    story.append(heading("Still Need Help?", styles))
    story.append(hrule())
    story.append(body(
        "If your issue is not listed above or you are unable to resolve it, "
        "please contact the Idox Geospatial support team:",
        styles,
    ))
    story.append(simple_table(
        headers=["Channel", "Details"],
        rows=[
            ["Email support", "geo-customersupport@idoxgroup.com"],
            ["SDK & documentation", "https://sdk.idoxgeospatial.co.uk/"],
        ],
        styles=styles,
        col_widths=[5 * cm, CONTENT_W - 5 * cm],
    ))
    story.append(Spacer(1, 0.3 * cm))
    story.append(body("When emailing support, please include:", styles))
    for item in [
        "Your full name and organisation",
        "Your ArcGIS Pro version (e.g., 3.2.0)",
        "Windows version (e.g., Windows 11 64-bit)",
        "A description of the problem",
        "Any error messages from the <b>Messages</b> panel in ArcGIS Pro",
    ]:
        story.append(bullet(item, styles))
    story.append(Spacer(1, 0.3 * cm))
    story.append(body("We aim to respond within one business day.", styles))

    doc.build(story)
    print(f"Created: {output_path}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    dist_dir = os.path.dirname(os.path.abspath(__file__))

    build_installation_guide(
        os.path.join(dist_dir, "Installation_and_Testing_Guide.pdf")
    )
    build_faq_guide(
        os.path.join(dist_dir, "FAQ_and_Troubleshooting.pdf")
    )
    print("All PDFs generated successfully.")
