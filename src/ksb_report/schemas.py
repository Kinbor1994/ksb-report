"""
KSB-Report — Schemas Pydantic
Defines the JSON contract for report generation.
"""

from __future__ import annotations

from typing import Annotated, Literal, Union

from pydantic import BaseModel, Discriminator, Field, Tag


# =============================================================================
# Font Configuration
# =============================================================================
class FontConfig(BaseModel):
    """Font configuration — use built-in Cambria or specify custom fonts."""

    family: str = "Cambria"
    regular: str | None = None
    bold: str | None = None
    italic: str | None = None
    bold_italic: str | None = None


# =============================================================================
# Color helpers
# =============================================================================
Color = tuple[int, int, int]


class ColorBarConfig(BaseModel):
    """Optional decorative color bar (e.g. Benin flag green/yellow/red)."""

    colors: list[Color] = []
    height: float = 2.0
    position: Literal["top", "bottom", "both"] = "top"


# =============================================================================
# Style Definition (reusable styles)
# =============================================================================
class StyleDef(BaseModel):
    """A reusable style definition that can be referenced by name."""

    font_size: float | None = None
    font_style: Literal["", "B", "I", "BI"] | None = None
    align: Literal["L", "C", "R"] | None = None
    color: Color | None = None
    bg_color: Color | None = None


# =============================================================================
# Watermark
# =============================================================================
class WatermarkConfig(BaseModel):
    """Watermark text drawn diagonally across every page."""

    text: str
    font_size: float = 60
    color: Color = (220, 220, 220)
    angle: float = 45
    opacity: float = 0.3


# =============================================================================
# Header / Footer
# =============================================================================
class HeaderLine(BaseModel):
    """A single line of text in the header."""

    text: str
    font_size: float = 11
    bold: bool = False
    italic: bool = False
    align: Literal["L", "C", "R"] = "C"


class HeaderConfig(BaseModel):
    """Fully customizable report header."""

    enabled: bool = True
    logo_left: str | None = None
    logo_right: str | None = None
    logo_width: float = 20
    logo_height: float = 20
    lines: list[HeaderLine] = []
    color_bar: ColorBarConfig | None = None
    separator_line: bool = True


class FooterConfig(BaseModel):
    """Fully customizable report footer."""

    enabled: bool = True
    left_text: str | None = None
    right_text: str | None = None
    show_page_number: bool = True
    show_date: bool = True
    date_format: str = "%d/%m/%Y"
    color_bar: ColorBarConfig | None = None
    separator_line: bool = True
    font_size: float = 8


# =============================================================================
# Margins
# =============================================================================
class MarginsConfig(BaseModel):
    """Page margins in mm."""

    top: float = 10
    bottom: float = 10
    left: float = 12.7
    right: float = 12.7


# =============================================================================
# Content Elements
# =============================================================================
class TextElement(BaseModel):
    """A block of text content."""

    type: Literal["text"] = "text"
    content: str
    font_size: float = 11
    font_style: Literal["", "B", "I", "BI"] = ""
    align: Literal["L", "C", "R"] = "L"
    color: Color | None = None
    style: str | None = None  # Reference to a named style


class TableElement(BaseModel):
    """A table with headers and data rows."""

    type: Literal["table"] = "table"
    headers: list[str]
    rows: list[list[str]]
    column_widths: list[float] | None = None
    column_types: list[Literal["text", "image"]] | None = None
    column_aligns: list[Literal["L", "C", "R"]] | None = None
    header_bg_color: Color = (70, 130, 180)
    header_text_color: Color = (255, 255, 255)
    striped_rows: bool = True
    stripe_color_even: Color = (248, 248, 248)
    stripe_color_odd: Color = (255, 255, 255)
    max_rows_per_page: int | None = None
    font_size: float = 10
    header_font_size: float = 10
    line_height: float = 5


class ImageElement(BaseModel):
    """An image element."""

    type: Literal["image"] = "image"
    path: str
    width: float | None = None
    height: float | None = None
    align: Literal["L", "C", "R"] = "C"


class SpacerElement(BaseModel):
    """Vertical spacing element."""

    type: Literal["spacer"] = "spacer"
    height: float = 10


class SectionTitleElement(BaseModel):
    """A styled section title with background."""

    type: Literal["section_title"] = "section_title"
    text: str
    font_size: float = 12
    bg_color: Color = (240, 240, 240)
    text_color: Color = (0, 0, 0)


class KeyValueElement(BaseModel):
    """Key-value pairs displayed in rows (e.g. invoice metadata)."""

    type: Literal["key_value"] = "key_value"
    pairs: list[tuple[str, str]]
    label_width: float = 40
    font_size: float = 10
    bold_labels: bool = True


class PageBreakElement(BaseModel):
    """Forces a new page."""

    type: Literal["page_break"] = "page_break"


class SeparatorElement(BaseModel):
    """A horizontal line separator."""

    type: Literal["separator"] = "separator"
    color: Color = (200, 200, 200)
    thickness: float = 0.5
    margin_top: float = 3
    margin_bottom: float = 3
    width_percent: float = 100  # % of available width


class ListElement(BaseModel):
    """A bullet or numbered list."""

    type: Literal["list"] = "list"
    items: list[str]
    list_style: Literal["bullet", "numbered", "dash"] = "bullet"
    font_size: float = 11
    indent: float = 10
    color: Color | None = None
    spacing: float = 2


class BoxElement(BaseModel):
    """A bordered box containing nested elements."""

    type: Literal["box"] = "box"
    elements: list[ContentElement] = []
    border_color: Color = (0, 0, 0)
    bg_color: Color | None = None
    border_width: float = 0.5
    padding: float = 5
    corner_radius: float = 0


class QRCodeElement(BaseModel):
    """A QR code generated from data."""

    type: Literal["qrcode"] = "qrcode"
    data: str
    size: float = 30
    align: Literal["L", "C", "R"] = "C"


class SignatureBlockElement(BaseModel):
    """One or more signature blocks side by side."""

    type: Literal["signature_block"] = "signature_block"
    signatures: list[SignatureEntry]
    line_width: float = 40
    spacing_top: float = 15  # Space above the line (for actual signature)


class SignatureEntry(BaseModel):
    """A single signature entry."""

    label: str  # e.g. "Le Directeur"
    name: str = ""  # e.g. "M. DUPONT"
    title: str = ""  # e.g. "Directeur Général"


class ColumnsElement(BaseModel):
    """Multi-column layout — elements rendered side by side."""

    type: Literal["columns"] = "columns"
    columns: list[ColumnDef]
    gap: float = 5  # Gap between columns in mm


class ColumnDef(BaseModel):
    """A single column definition with width and nested elements."""

    width: float = 50  # Width as percentage (0-100)
    elements: list[ContentElement] = []


# =============================================================================
# Discriminated Union of all content element types
# =============================================================================
def _get_element_type(v):
    if isinstance(v, dict):
        return v.get("type")
    return getattr(v, "type", None)


ContentElement = Annotated[
    Union[
        Annotated[TextElement, Tag("text")],
        Annotated[TableElement, Tag("table")],
        Annotated[ImageElement, Tag("image")],
        Annotated[SpacerElement, Tag("spacer")],
        Annotated[SectionTitleElement, Tag("section_title")],
        Annotated[KeyValueElement, Tag("key_value")],
        Annotated[PageBreakElement, Tag("page_break")],
        Annotated[SeparatorElement, Tag("separator")],
        Annotated[ListElement, Tag("list")],
        Annotated[BoxElement, Tag("box")],
        Annotated[QRCodeElement, Tag("qrcode")],
        Annotated[SignatureBlockElement, Tag("signature_block")],
        Annotated[ColumnsElement, Tag("columns")],
    ],
    Discriminator(_get_element_type),
]

# Update forward references for recursive types
BoxElement.model_rebuild()
ColumnsElement.model_rebuild()
ColumnDef.model_rebuild()
SignatureBlockElement.model_rebuild()


# =============================================================================
# Page Configuration
# =============================================================================
class PageConfig(BaseModel):
    """Page layout configuration."""

    orientation: Literal["portrait", "landscape"] = "portrait"
    format: Literal["A4", "A3", "Letter"] = "A4"
    margins: MarginsConfig = Field(default_factory=MarginsConfig)


# =============================================================================
# Main Report Template
# =============================================================================
class ReportTemplate(BaseModel):
    """
    The main contract — everything needed to describe a report.
    Send this as JSON to the API or pass it to ReportEngine.generate().
    """

    page: PageConfig = Field(default_factory=PageConfig)
    font: FontConfig = Field(default_factory=FontConfig)
    header: HeaderConfig | None = None
    footer: FooterConfig | None = None
    title: str | None = None
    title_font_size: float = 14
    title_align: Literal["L", "C", "R"] = "C"
    elements: list[ContentElement] = []
    metadata: dict[str, str] = {}
    watermark: WatermarkConfig | None = None
    variables: dict[str, str] = {}
    styles: dict[str, StyleDef] = {}
