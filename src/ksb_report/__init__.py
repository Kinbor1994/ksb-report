"""
KSB-Report — Python library + API for generating customizable PDF reports.
"""

from ksb_report.engine import ReportEngine
from ksb_report.schemas import (
    BoxElement,
    ColorBarConfig,
    ColumnDef,
    ColumnsElement,
    ContentElement,
    FontConfig,
    FooterConfig,
    HeaderConfig,
    HeaderLine,
    ImageElement,
    KeyValueElement,
    ListElement,
    MarginsConfig,
    PageBreakElement,
    PageConfig,
    QRCodeElement,
    ReportTemplate,
    SectionTitleElement,
    SeparatorElement,
    SignatureBlockElement,
    SignatureEntry,
    SpacerElement,
    StyleDef,
    TableElement,
    TextElement,
    WatermarkConfig,
)

__version__ = "0.1.0"

__all__ = [
    # Engine
    "ReportEngine",
    # Template & Config
    "ReportTemplate",
    "PageConfig",
    "FontConfig",
    "HeaderConfig",
    "HeaderLine",
    "FooterConfig",
    "MarginsConfig",
    "ColorBarConfig",
    "WatermarkConfig",
    "StyleDef",
    # Elements
    "ContentElement",
    "TextElement",
    "TableElement",
    "ImageElement",
    "SpacerElement",
    "SectionTitleElement",
    "KeyValueElement",
    "PageBreakElement",
    "SeparatorElement",
    "ListElement",
    "BoxElement",
    "QRCodeElement",
    "SignatureBlockElement",
    "SignatureEntry",
    "ColumnsElement",
    "ColumnDef",
]
