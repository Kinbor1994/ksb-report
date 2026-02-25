"""
Tests for FastAPI endpoints.
"""

import pytest
from fastapi.testclient import TestClient

from ksb_report.api import app


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


class TestHealthEndpoint:
    def test_health(self, client):
        response = client.get("/api/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "version" in data


class TestGenerateEndpoint:
    def test_generate_minimal(self, client):
        """POST with minimal template should return a PDF."""
        response = client.post(
            "/api/reports/generate",
            json={"elements": []},
        )
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/pdf"
        assert response.content[:5] == b"%PDF-"

    def test_generate_with_content(self, client):
        """POST with content should return a valid PDF."""
        payload = {
            "title": "API Test Report",
            "elements": [
                {"type": "text", "content": "Hello from API"},
                {
                    "type": "table",
                    "headers": ["A", "B"],
                    "rows": [["1", "2"]],
                },
            ],
        }
        response = client.post("/api/reports/generate", json=payload)
        assert response.status_code == 200
        assert response.content[:5] == b"%PDF-"
        assert len(response.content) > 500

    def test_generate_custom_filename(self, client):
        """Custom filename in metadata should appear in Content-Disposition."""
        payload = {
            "elements": [],
            "metadata": {"filename": "my_report.pdf"},
        }
        response = client.post("/api/reports/generate", json=payload)
        assert response.status_code == 200
        assert "my_report.pdf" in response.headers.get("content-disposition", "")

    def test_generate_invalid_payload(self, client):
        """Invalid element type should fail validation."""
        payload = {
            "elements": [{"type": "nonexistent", "content": "bad"}],
        }
        response = client.post("/api/reports/generate", json=payload)
        assert response.status_code == 422

    def test_generate_full_report(self, client):
        """Full report with header, footer, and multiple elements."""
        payload = {
            "title": "Full API Report",
            "header": {
                "lines": [
                    {"text": "Company Name", "font_size": 16, "bold": True},
                ],
            },
            "footer": {
                "left_text": "Generated via API",
                "show_date": True,
            },
            "elements": [
                {"type": "section_title", "text": "Section 1"},
                {"type": "text", "content": "Hello"},
                {"type": "key_value", "pairs": [["Key", "Value"]]},
                {
                    "type": "table",
                    "headers": ["Name", "Score"],
                    "rows": [["Alice", "95"], ["Bob", "87"]],
                },
            ],
        }
        response = client.post("/api/reports/generate", json=payload)
        assert response.status_code == 200
        assert response.content[:5] == b"%PDF-"


class TestPreviewEndpoint:
    def test_preview_inline(self, client):
        """Preview should return PDF with inline disposition."""
        response = client.post(
            "/api/reports/preview",
            json={"elements": [{"type": "text", "content": "Preview test"}]},
        )
        assert response.status_code == 200
        assert response.content[:5] == b"%PDF-"
        assert "inline" in response.headers.get("content-disposition", "")
