# KSB-Report

API + bibliothèque Python pour générer des rapports PDF 100% personnalisables.

## Installation

```bash
pip install ksb-report
```

## Utilisation rapide

### En tant que bibliothèque Python

```python
from ksb_report import ReportEngine, ReportTemplate

template = ReportTemplate(
    title="Mon Rapport",
    elements=[
        {"type": "text", "content": "Bonjour le monde !"},
        {
            "type": "table",
            "headers": ["Nom", "Score"],
            "rows": [["Alice", "95"], ["Bob", "87"]],
        },
    ],
)

engine = ReportEngine()
pdf_bytes = engine.generate(template)

# Sauvegarder sur disque
engine.generate_to_file(template, "rapport.pdf")
```

### Template facture pré-construit

```python
from ksb_report import ReportEngine
from ksb_report.templates import invoice_template

template = invoice_template(
    company_name="Ma Société",
    invoice_number="2026-001",
    client_name="Jean Dupont",
    items=[
        {"description": "Widget A", "quantity": 2, "unit_price": 15.00},
        {"description": "Service B", "quantity": 1, "unit_price": 50.00},
    ],
    tax_rate=0.18,
)

engine = ReportEngine()
engine.generate_to_file(template, "facture.pdf")
```

### API HTTP

```bash
# Lancer le serveur
ksb-report serve --port 8500

# Générer un PDF via curl
curl -X POST http://localhost:8500/api/reports/generate \
  -H "Content-Type: application/json" \
  -d '{"title": "Test", "elements": [{"type": "text", "content": "Hello"}]}' \
  -o rapport.pdf
```

### CLI — Générer depuis un fichier JSON

```bash
ksb-report generate template.json -o output.pdf
```

## Développement

```bash
pip install -e ".[dev]"
pytest
```
