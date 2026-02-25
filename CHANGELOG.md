# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial project scaffold
- Core PDF engine with FPDF2 wrapper (`KSBReport`)
- Pydantic schemas for JSON-driven report generation
- Content elements: text, tables, images, QR codes, spacers, page breaks
- Customizable headers and footers
- Embedded font support (DejaVu Sans)
- Template system (Invoice, Report Card)
- FastAPI HTTP API for PDF generation
- CLI tool (`ksb-report serve` / `ksb-report generate`)
