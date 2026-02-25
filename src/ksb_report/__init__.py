"""
KSB-Report — Python library + API for generating customizable PDF reports.
"""

from ksb_report.engine import ReportEngine
from ksb_report.schemas import (
    ColorBarConfig,
    ContentElement,
    FontConfig,
    FooterConfig,
    HeaderConfig,
    HeaderLine,
    ImageElement,
    KeyValueElement,
    MarginsConfig,
    PageConfig,
    ReportTemplate,
    SectionTitleElement,
    SpacerElement,
    TableElement,
    TextElement,
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
    # Elements
    "ContentElement",
    "TextElement",
    "TableElement",
    "ImageElement",
    "SpacerElement",
    "SectionTitleElement",
    "KeyValueElement",
]
