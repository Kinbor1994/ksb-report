"""
KSB-Report — ReportEngine
Orchestrator that takes a ReportTemplate and produces PDF bytes.
"""

from __future__ import annotations

from pathlib import Path

from ksb_report.pdf import ReportFPDF
from ksb_report.schemas import (
    ContentElement,
    ImageElement,
    KeyValueElement,
    ReportTemplate,
    SectionTitleElement,
    SpacerElement,
    TableElement,
    TextElement,
)


class ReportEngine:
    """
    Main entry point for PDF generation.

    Usage:
        engine = ReportEngine()
        pdf_bytes = engine.generate(template)
        engine.generate_to_file(template, "output.pdf")
    """

    def generate(self, template: ReportTemplate) -> bytes:
        """Generate a PDF from a ReportTemplate. Returns raw PDF bytes."""
        pdf = ReportFPDF(template)
        pdf.add_page()

        # Render title if provided
        if template.title:
            pdf.render_title(
                template.title,
                font_size=template.title_font_size,
                align=template.title_align,
            )

        # Render all content elements
        for element in template.elements:
            self._render_element(pdf, element)

        return bytes(pdf.output())

    def generate_to_file(self, template: ReportTemplate, path: str) -> str:
        """Generate a PDF and save to disk. Returns the output path."""
        data = self.generate(template)
        output = Path(path)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(data)
        return str(output)

    def _render_element(self, pdf: ReportFPDF, element: ContentElement) -> None:
        """Dispatch rendering to the appropriate method based on element type."""
        if isinstance(element, TextElement):
            pdf.render_text(
                content=element.content,
                font_size=element.font_size,
                font_style=element.font_style,
                align=element.align,
                color=element.color,
            )

        elif isinstance(element, TableElement):
            pdf.render_table(
                headers=element.headers,
                rows=element.rows,
                column_widths=element.column_widths,
                column_types=element.column_types,
                header_bg_color=element.header_bg_color,
                header_text_color=element.header_text_color,
                striped_rows=element.striped_rows,
                stripe_color_even=element.stripe_color_even,
                stripe_color_odd=element.stripe_color_odd,
                max_rows_per_page=element.max_rows_per_page,
                font_size=element.font_size,
                header_font_size=element.header_font_size,
                line_height=element.line_height,
            )

        elif isinstance(element, ImageElement):
            pdf.render_image(
                path=element.path,
                width=element.width,
                height=element.height,
                align=element.align,
            )

        elif isinstance(element, SpacerElement):
            pdf.ln(element.height)

        elif isinstance(element, SectionTitleElement):
            pdf.render_section_title(
                text=element.text,
                font_size=element.font_size,
                bg_color=element.bg_color,
                text_color=element.text_color,
            )

        elif isinstance(element, KeyValueElement):
            pdf.render_key_value(
                pairs=element.pairs,
                label_width=element.label_width,
                font_size=element.font_size,
                bold_labels=element.bold_labels,
            )
