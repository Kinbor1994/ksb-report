# Security Policy

## Supported Versions

| Version | Supported          |
|---------|--------------------|
| 0.1.x   | ✅ Current         |

## Reporting a Vulnerability

If you discover a security vulnerability in KSB-Report, please report it responsibly.

**Do NOT open a public issue.**

Instead, email **kinnoumeb@gmail.com** with:

- A description of the vulnerability
- Steps to reproduce the issue
- Impact assessment (if known)

You will receive an acknowledgment within **48 hours** and a detailed response
within **7 days** indicating next steps.

## Security Considerations

KSB-Report generates PDF files from user-provided JSON templates. Please note:

- **File paths**: The `image` element accepts file paths. In server mode, validate and restrict paths to prevent directory traversal.
- **QR codes**: QR code data is rendered as-is. Validate URLs before passing them to templates.
- **Template injection**: The `{{variable}}` system only replaces known keys. Unknown keys are left untouched (no code execution).
