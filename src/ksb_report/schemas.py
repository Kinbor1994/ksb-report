"""
KSB-Report — Schemas Pydantic
Defines the JSON contract for report generation.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


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


class TableElement(BaseModel):
    """A table with headers and data rows."""

    type: Literal["table"] = "table"
    headers: list[str]
    rows: list[list[str]]
    column_widths: list[float] | None = None
    column_types: list[Literal["text", "image"]] | None = None
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


# Union of all content element types
ContentElement = (
    TextElement
    | TableElement
    | ImageElement
    | SpacerElement
    | SectionTitleElement
    | KeyValueElement
)


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
