"""
KSB-Report — ReportEngine
Orchestrator that takes a ReportTemplate and produces PDF bytes.
Handles variable resolution, style application, and element dispatching.
"""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any

from ksb_report.pdf import ReportFPDF
from ksb_report.schemas import (
    BoxElement,
    ColumnsElement,
    ContentElement,
    ImageElement,
    KeyValueElement,
    ListElement,
    PageBreakElement,
    QRCodeElement,
    ReportTemplate,
    SectionTitleElement,
    SeparatorElement,
    SignatureBlockElement,
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

    # Built-in variables resolved automatically
    _BUILTIN_VARS = {
        "current_date",
        "current_time",
        "current_datetime",
        "year",
        "month",
        "day",
    }

    def generate(self, template: ReportTemplate) -> bytes:
        """Generate a PDF from a ReportTemplate. Returns raw PDF bytes."""
        # Resolve variables in the entire template
        resolved = self._resolve_variables(template)

        pdf = ReportFPDF(resolved)
        pdf.add_page()

        # Watermark on first page
        if resolved.watermark:
            pdf.render_watermark(resolved.watermark)

        # Render title if provided
        if resolved.title:
            pdf.render_title(
                resolved.title,
                font_size=resolved.title_font_size,
                align=resolved.title_align,
            )

        # Render all content elements
        for element in resolved.elements:
            self._render_element(pdf, element)

        result = bytes(pdf.output())
        pdf.cleanup()
        return result

    def generate_to_file(self, template: ReportTemplate, path: str) -> str:
        """Generate a PDF and save to disk. Returns the output path."""
        data = self.generate(template)
        output = Path(path)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(data)
        return str(output)

    # =========================================================================
    # Variable Resolution
    # =========================================================================
    def _resolve_variables(self, template: ReportTemplate) -> ReportTemplate:
        """
        Resolve {{variable}} placeholders throughout the template.
        Combines built-in variables with user-defined ones.
        """
        if not template.variables and not any(
            var in json.dumps(template.model_dump(mode="json")) for var in ["{{"]
        ):
            return template  # No variables to resolve, short-circuit

        # Build the variable map
        now = datetime.now()
        var_map = {
            "current_date": now.strftime("%d/%m/%Y"),
            "current_time": now.strftime("%H:%M"),
            "current_datetime": now.strftime("%d/%m/%Y %H:%M"),
            "year": str(now.year),
            "month": str(now.month).zfill(2),
            "day": str(now.day).zfill(2),
        }
        # User variables override built-ins
        var_map.update(template.variables)

        # Serialize to JSON, replace all {{key}} patterns, deserialize back
        raw = template.model_dump(mode="json")
        raw_json = json.dumps(raw, ensure_ascii=False)

        for key, value in var_map.items():
            raw_json = raw_json.replace("{{" + key + "}}", value)

        # Replace any remaining unknown variables with empty string
        raw_json = re.sub(r"\{\{[^}]+\}\}", "", raw_json)

        resolved_data = json.loads(raw_json)
        return ReportTemplate(**resolved_data)

    # =========================================================================
    # Element Dispatching
    # =========================================================================
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
                column_aligns=element.column_aligns,
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

        elif isinstance(element, PageBreakElement):
            pdf.add_page()
            # Re-apply watermark on new page
            if pdf.template.watermark:
                pdf.render_watermark(pdf.template.watermark)

        elif isinstance(element, SeparatorElement):
            pdf.render_separator(
                color=element.color,
                thickness=element.thickness,
                margin_top=element.margin_top,
                margin_bottom=element.margin_bottom,
                width_percent=element.width_percent,
            )

        elif isinstance(element, ListElement):
            pdf.render_list(
                items=element.items,
                list_style=element.list_style,
                font_size=element.font_size,
                indent=element.indent,
                color=element.color,
                spacing=element.spacing,
            )

        elif isinstance(element, BoxElement):
            pdf.render_box(
                render_elements_fn=lambda el: self._render_element(pdf, el),
                elements=element.elements,
                border_color=element.border_color,
                bg_color=element.bg_color,
                border_width=element.border_width,
                padding=element.padding,
                corner_radius=element.corner_radius,
            )

        elif isinstance(element, ColumnsElement):
            pdf.render_columns(
                render_elements_fn=lambda el: self._render_element(pdf, el),
                columns=element.columns,
                gap=element.gap,
            )

        elif isinstance(element, QRCodeElement):
            pdf.render_qrcode(
                data=element.data,
                size=element.size,
                align=element.align,
            )

        elif isinstance(element, SignatureBlockElement):
            pdf.render_signature_block(
                signatures=element.signatures,
                line_width=element.line_width,
                spacing_top=element.spacing_top,
            )
