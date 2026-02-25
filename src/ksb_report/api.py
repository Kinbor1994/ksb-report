"""
KSB-Report — FastAPI HTTP API
POST a JSON ReportTemplate, get back a PDF.
"""

from __future__ import annotations

import io
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from ksb_report import __version__
from ksb_report.engine import ReportEngine
from ksb_report.schemas import ReportTemplate


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup / shutdown events."""
    app.state.engine = ReportEngine()
    yield


app = FastAPI(
    title="KSB-Report API",
    version=__version__,
    description="Generate customizable PDF reports from JSON templates.",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
async def health():
    """Health check endpoint."""
    return {"status": "ok", "version": __version__}


@app.post("/api/reports/generate")
async def generate_report(template: ReportTemplate):
    """
    Generate a PDF report from a JSON template.

    Returns the PDF as a streaming binary response.
    """
    engine: ReportEngine = app.state.engine
    pdf_bytes = engine.generate(template)

    filename = template.metadata.get("filename", "report.pdf")
    if not filename.endswith(".pdf"):
        filename += ".pdf"

    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@app.post("/api/reports/preview")
async def preview_report(template: ReportTemplate):
    """
    Generate a PDF report for inline preview (no download prompt).
    """
    engine: ReportEngine = app.state.engine
    pdf_bytes = engine.generate(template)

    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={"Content-Disposition": "inline"},
    )
