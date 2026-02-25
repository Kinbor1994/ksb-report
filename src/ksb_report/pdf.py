"""
KSB-Report — ReportFPDF
Unified FPDF class handling header, footer, tables, text, and images.
Inspired by school_desk's BulletinFPDF and CustomFPDF, but fully decoupled.
"""

from __future__ import annotations

import os
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any

from fpdf import FPDF

if TYPE_CHECKING:
    from ksb_report.schemas import (
        ColorBarConfig,
        FooterConfig,
        HeaderConfig,
        ReportTemplate,
    )

FONTS_DIR = Path(__file__).parent / "fonts"


class ReportFPDF(FPDF):
    """
    Custom FPDF class that renders headers, footers, and content
    based on a ReportTemplate configuration.
    """

    def __init__(self, template: ReportTemplate):
        orientation = "L" if template.page.orientation == "landscape" else "P"
        super().__init__(orientation=orientation, unit="mm", format=template.page.format)

        self.template = template
        self._font_family_name = template.font.family
        self._fonts_loaded = False

        # Margins
        m = template.page.margins
        self.set_margins(m.left, m.top, m.right)
        self.set_auto_page_break(auto=True, margin=m.bottom + 15)

        # Load fonts
        self._load_fonts()

    # =========================================================================
    # Font Loading
    # =========================================================================
    def _load_fonts(self) -> None:
        """Load custom fonts from the fonts directory or user-specified paths."""
        font_config = self.template.font
        family = font_config.family

        # Try user-specified font paths first
        if font_config.regular:
            try:
                self._register_font_variant(family, "", font_config.regular)
                if font_config.bold:
                    self._register_font_variant(family, "B", font_config.bold)
                if font_config.italic:
                    self._register_font_variant(family, "I", font_config.italic)
                if font_config.bold_italic:
                    self._register_font_variant(family, "BI", font_config.bold_italic)
                self._fonts_loaded = True
                self.set_font(family, "", 10)
                return
            except Exception:
                pass

        # Try built-in Cambria
        if family.lower() == "cambria":
            try:
                self.add_font("Cambria", "", str(FONTS_DIR / "cambria.ttc"))
                self.add_font("Cambria", "B", str(FONTS_DIR / "cambriab.ttf"))
                self.add_font("Cambria", "I", str(FONTS_DIR / "cambriai.ttf"))
                self.add_font("Cambria", "BI", str(FONTS_DIR / "cambriaz.ttf"))
                self._font_family_name = "Cambria"
                self._fonts_loaded = True
                self.set_font("Cambria", "", 10)
                return
            except Exception:
                pass

        # Fallback to Helvetica
        self._font_family_name = "Helvetica"
        self._fonts_loaded = True
        self.set_font("Helvetica", "", 10)

    def _register_font_variant(self, family: str, style: str, path: str) -> None:
        """Register a single font variant."""
        if Path(path).exists():
            self.add_font(family, style, path)

    @property
    def font_name(self) -> str:
        return self._font_family_name

    # =========================================================================
    # Header
    # =========================================================================
    def header(self) -> None:
        hdr = self.template.header
        if not hdr or not hdr.enabled:
            return

        start_y = self.get_y()

        # Color bar at top
        if hdr.color_bar and hdr.color_bar.position in ("top", "both"):
            self._draw_color_bar(hdr.color_bar, y=start_y + 2)
            start_y += hdr.color_bar.height + 3

        # Logo left
        logo_y = start_y + 3
        text_x_start = self.l_margin
        text_x_end = self.w - self.r_margin

        if hdr.logo_left and os.path.exists(hdr.logo_left):
            try:
                self.image(
                    hdr.logo_left,
                    x=self.l_margin,
                    y=logo_y,
                    w=hdr.logo_width,
                    h=hdr.logo_height,
                )
            except Exception:
                self._draw_logo_placeholder(
                    self.l_margin, logo_y, hdr.logo_width, hdr.logo_height
                )
            text_x_start = self.l_margin + hdr.logo_width + 5

        # Logo right
        if hdr.logo_right and os.path.exists(hdr.logo_right):
            logo_x = self.w - self.r_margin - hdr.logo_width
            try:
                self.image(
                    hdr.logo_right,
                    x=logo_x,
                    y=logo_y,
                    w=hdr.logo_width,
                    h=hdr.logo_height,
                )
            except Exception:
                self._draw_logo_placeholder(
                    logo_x, logo_y, hdr.logo_width, hdr.logo_height
                )
            text_x_end = logo_x - 5

        text_width = text_x_end - text_x_start

        # Header text lines
        current_y = logo_y
        for line in hdr.lines:
            style = ""
            if line.bold:
                style += "B"
            if line.italic:
                style += "I"
            self.set_font(self.font_name, style, line.font_size)
            self.set_xy(text_x_start, current_y)
            self.multi_cell(text_width, line.font_size * 0.5, line.text, align=line.align)
            current_y = self.get_y()

        # Separator line
        header_bottom = max(current_y, logo_y + hdr.logo_height) + 2
        if hdr.separator_line:
            self.set_draw_color(0, 0, 0)
            self.line(self.l_margin, header_bottom, self.w - self.r_margin, header_bottom)

        self.set_y(header_bottom + 3)

    # =========================================================================
    # Footer
    # =========================================================================
    def footer(self) -> None:
        ftr = self.template.footer
        if not ftr or not ftr.enabled:
            return

        self.set_y(-15)
        self.set_font(self.font_name, "I", ftr.font_size)
        self.set_text_color(128, 128, 128)

        # Separator line
        if ftr.separator_line:
            self.set_draw_color(180, 180, 180)
            self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
            self.ln(1)

        # Left text
        left_text = ftr.left_text or ""
        if ftr.show_date:
            date_str = datetime.now().strftime(ftr.date_format)
            if left_text:
                left_text = f"{left_text} — {date_str}"
            else:
                left_text = date_str

        self.cell(0, 5, left_text, align="L")

        # Right text (page number)
        right_text = ftr.right_text or f"Page {self.page_no()}/{{nb}}"
        right_text = right_text.replace("{page}", str(self.page_no()))
        right_text = right_text.replace("{pages}", str(self.pages_count))
        self.cell(0, 5, right_text, align="R")

        # Color bar at bottom
        if ftr.color_bar and ftr.color_bar.position in ("bottom", "both"):
            self._draw_color_bar(ftr.color_bar, y=self.h - 8)

        self.set_text_color(0, 0, 0)

    # =========================================================================
    # Drawing Helpers
    # =========================================================================
    def _draw_color_bar(self, config: ColorBarConfig, y: float) -> None:
        """Draw a horizontal multi-colored bar (e.g. national flag colors)."""
        if not config.colors:
            return
        total_width = 60
        bar_width = total_width / len(config.colors)
        x_start = (self.w - total_width) / 2
        for i, color in enumerate(config.colors):
            self.set_fill_color(*color)
            self.rect(x_start + i * bar_width, y, bar_width, config.height, "F")

    def _draw_logo_placeholder(
        self, x: float, y: float, w: float, h: float
    ) -> None:
        """Draw a placeholder rectangle where a logo should be."""
        self.set_draw_color(200, 200, 200)
        self.rect(x, y, w, h)
        self.set_font(self.font_name, "", 8)
        text = "LOGO"
        self.text(x + (w - self.get_string_width(text)) / 2, y + h / 2 + 2, text)

    # =========================================================================
    # Content Rendering Methods
    # =========================================================================
    def render_title(self, title: str, font_size: float = 14, align: str = "C") -> None:
        """Render the report title."""
        self.set_font(self.font_name, "B", font_size)
        self.cell(0, font_size * 0.7, title, align=align, new_x="LMARGIN", new_y="NEXT")
        self.ln(5)

    def render_text(
        self,
        content: str,
        font_size: float = 11,
        font_style: str = "",
        align: str = "L",
        color: tuple[int, int, int] | None = None,
    ) -> None:
        """Render a text block."""
        if color:
            self.set_text_color(*color)
        self.set_font(self.font_name, font_style, font_size)
        self.multi_cell(0, font_size * 0.5, content, align=align)
        if color:
            self.set_text_color(0, 0, 0)
        self.ln(3)

    def render_section_title(
        self,
        text: str,
        font_size: float = 12,
        bg_color: tuple[int, int, int] = (240, 240, 240),
        text_color: tuple[int, int, int] = (0, 0, 0),
    ) -> None:
        """Render a styled section title with background."""
        self.set_font(self.font_name, "B", font_size)
        self.set_fill_color(*bg_color)
        self.set_text_color(*text_color)
        self.cell(0, 8, f"  {text}", ln=True, fill=True)
        self.set_text_color(0, 0, 0)
        self.ln(2)

    def render_key_value(
        self,
        pairs: list[tuple[str, str]],
        label_width: float = 40,
        font_size: float = 10,
        bold_labels: bool = True,
    ) -> None:
        """Render key-value pairs."""
        for label, value in pairs:
            self.set_font(self.font_name, "B" if bold_labels else "", font_size)
            self.cell(label_width, font_size * 0.6, f"{label} :")
            self.set_font(self.font_name, "", font_size)
            self.cell(0, font_size * 0.6, value, new_x="LMARGIN", new_y="NEXT")
        self.ln(3)

    def render_image(
        self,
        path: str,
        width: float | None = None,
        height: float | None = None,
        align: str = "C",
    ) -> None:
        """Render an image."""
        if not os.path.exists(path):
            self._draw_logo_placeholder(
                self.get_x(), self.get_y(), width or 40, height or 30
            )
            return

        x = self.l_margin
        if align == "C" and width:
            x = (self.w - width) / 2
        elif align == "R" and width:
            x = self.w - self.r_margin - width

        kwargs: dict[str, Any] = {"x": x, "y": self.get_y()}
        if width:
            kwargs["w"] = width
        if height:
            kwargs["h"] = height

        try:
            self.image(path, **kwargs)
            self.ln((height or 20) + 3)
        except Exception:
            self._draw_logo_placeholder(x, self.get_y(), width or 40, height or 30)

    def render_table(
        self,
        headers: list[str],
        rows: list[list[str]],
        column_widths: list[float] | None = None,
        column_types: list[str] | None = None,
        header_bg_color: tuple[int, int, int] = (70, 130, 180),
        header_text_color: tuple[int, int, int] = (255, 255, 255),
        striped_rows: bool = True,
        stripe_color_even: tuple[int, int, int] = (248, 248, 248),
        stripe_color_odd: tuple[int, int, int] = (255, 255, 255),
        max_rows_per_page: int | None = None,
        font_size: float = 10,
        header_font_size: float = 10,
        line_height: float = 5,
    ) -> None:
        """
        Render a table with auto-pagination and header re-drawing.
        Handles dynamic row heights from multi-line cells.
        """
        if not headers or not rows:
            return

        available_width = self.w - self.l_margin - self.r_margin
        col_widths = self._compute_column_widths(
            headers, column_widths, column_types, available_width
        )

        def draw_table_headers() -> None:
            self.set_font(self.font_name, "B", header_font_size)
            self.set_fill_color(*header_bg_color)
            self.set_text_color(*header_text_color)

            # Calculate header height based on content
            max_lines = 1
            for i, hdr_text in enumerate(headers):
                lines = self.multi_cell(
                    col_widths[i] - 2, line_height, hdr_text, dry_run=True, output="LINES"
                )
                max_lines = max(max_lines, len(lines))
            header_height = max_lines * line_height + 4

            x_start = self.get_x()
            y_start = self.get_y()

            # Draw background rectangles
            for i, cw in enumerate(col_widths):
                self.rect(
                    x_start + sum(col_widths[:i]),
                    y_start, cw, header_height, style="DF"
                )

            # Draw header text centered vertically
            for i, hdr_text in enumerate(headers):
                cell_x = x_start + sum(col_widths[:i])
                lines = self.multi_cell(
                    col_widths[i] - 2, line_height, hdr_text, dry_run=True, output="LINES"
                )
                text_h = len(lines) * line_height
                y_pos = y_start + (header_height - text_h) / 2
                self.set_xy(cell_x + 1, y_pos)
                self.multi_cell(col_widths[i] - 2, line_height, hdr_text, align="C")

            self.set_xy(x_start, y_start + header_height)
            self.set_text_color(0, 0, 0)

        draw_table_headers()
        rows_on_page = 0

        for row_idx, row in enumerate(rows):
            self.set_font(self.font_name, "", font_size)

            # Calculate row height
            num_lines = 1
            for i, cell_data in enumerate(row):
                if i < len(col_widths):
                    lines = self.multi_cell(
                        col_widths[i] - 2, line_height, str(cell_data),
                        dry_run=True, output="LINES"
                    )
                    num_lines = max(num_lines, len(lines))
            row_height = num_lines * line_height + 4

            # Check for page break
            needs_break = (
                (max_rows_per_page and rows_on_page >= max_rows_per_page)
                or (self.get_y() + row_height > self.h - self.b_margin)
            )

            if needs_break:
                self.add_page()
                draw_table_headers()
                rows_on_page = 0

            # Row background
            if striped_rows:
                bg = stripe_color_even if row_idx % 2 == 0 else stripe_color_odd
                self.set_fill_color(*bg)
            else:
                self.set_fill_color(255, 255, 255)

            x_start = self.get_x()
            y_start = self.get_y()

            # Draw cell backgrounds
            for i, cw in enumerate(col_widths):
                self.rect(
                    x_start + sum(col_widths[:i]),
                    y_start, cw, row_height, "DF"
                )

            # Draw cell text
            self.set_font(self.font_name, "", font_size)
            for i, cell_data in enumerate(row):
                if i >= len(col_widths):
                    break
                cell_x = x_start + sum(col_widths[:i])
                cell_text = str(cell_data)

                # Handle image columns
                if column_types and i < len(column_types) and column_types[i] == "image":
                    self._draw_image_in_table_cell(
                        cell_text, cell_x, y_start, col_widths[i], row_height
                    )
                else:
                    # Center text vertically in cell
                    lines = self.multi_cell(
                        col_widths[i] - 2, line_height, cell_text,
                        dry_run=True, output="LINES"
                    )
                    text_h = len(lines) * line_height
                    y_pos = y_start + (row_height - text_h) / 2
                    self.set_xy(cell_x + 1, y_pos)
                    self.multi_cell(col_widths[i] - 2, line_height, cell_text, align="L")

            self.set_y(y_start + row_height)
            rows_on_page += 1

        self.ln(5)

    def _compute_column_widths(
        self,
        headers: list[str],
        user_widths: list[float] | None,
        column_types: list[str] | None,
        available_width: float,
    ) -> list[float]:
        """Compute final column widths from user percentages or auto-distribute."""
        n = len(headers)
        if user_widths and len(user_widths) == n:
            total = sum(user_widths)
            if total <= 100:
                return [(w / total) * available_width for w in user_widths]
            return user_widths[:n]
        return [available_width / n] * n

    def _draw_image_in_table_cell(
        self,
        image_path: str,
        x: float,
        y: float,
        width: float,
        height: float,
    ) -> None:
        """Draw an image centered in a table cell."""
        img_size = min(width, height) - 4
        img_x = x + (width - img_size) / 2
        img_y = y + (height - img_size) / 2
        if image_path and os.path.exists(image_path):
            try:
                self.image(image_path, x=img_x, y=img_y, w=img_size, h=img_size)
                return
            except Exception:
                pass
        # Placeholder
        self._draw_logo_placeholder(img_x, img_y, img_size, img_size)
