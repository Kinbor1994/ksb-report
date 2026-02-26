# KSB-Report

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Tests](https://github.com/Kinbor1994/ksb-report/actions/workflows/ci.yml/badge.svg)](https://github.com/Kinbor1994/ksb-report/actions/workflows/ci.yml)
[![PyPI version](https://img.shields.io/pypi/v/ksb-report.svg)](https://pypi.org/project/ksb-report/)

**API + bibliothèque Python pour générer des rapports PDF professionnels, 100% personnalisables via JSON.**

Définissez vos rapports en JSON — titres, tableaux, colonnes, QR codes, signatures, watermarks — et obtenez un PDF pixel-perfect en une ligne de code.

---

## ✨ Fonctionnalités

| Catégorie | Fonctionnalités |
|-----------|----------------|
| **13 types d'éléments** | Texte, Table, Image, Spacer, Section Title, Key-Value, Page Break, Separator, List, Box, Columns, QR Code, Signature Block |
| **Layout avancé** | Colonnes multi-positions, boîtes avec bordures, sauts de page forcés |
| **Variables dynamiques** | `{{current_date}}`, `{{year}}`, `{{page_number}}` + variables custom |
| **Watermark** | Filigrane diagonal configurable sur chaque page |
| **Tables riches** | Alignement par colonne (L/C/R), lignes striées, auto-pagination avec en-têtes |
| **Header/Footer** | Logos, couleurs, barre de couleur, séparateur, numérotation automatique |
| **Templates** | Facture pré-construite, extensible |
| **3 interfaces** | Bibliothèque Python • API HTTP (FastAPI) • CLI |

---

## 📦 Installation

```bash
pip install ksb-report
```

Depuis les sources :

```bash
git clone https://github.com/Kinbor1994/ksb-report.git
cd ksb-report
pip install -e ".[dev]"
```

---

## 🚀 Quick Start

### Bibliothèque Python

```python
from ksb_report import ReportEngine, ReportTemplate

template = ReportTemplate(
    title="Mon Rapport",
    elements=[
        {"type": "text", "content": "Bonjour le monde !", "font_size": 14},
        {
            "type": "table",
            "headers": ["Nom", "Score"],
            "rows": [["Alice", "95"], ["Bob", "87"]],
            "header_bg_color": [41, 128, 185],
            "header_text_color": [255, 255, 255],
        },
        {"type": "qrcode", "data": "https://example.com", "size": 25},
    ],
)

engine = ReportEngine()

# En mémoire (bytes)
pdf_bytes = engine.generate(template)

# Ou directement sur disque
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

---

## 📘 Éléments disponibles

| Type | Description | Paramètres clés |
|------|-------------|-----------------|
| `text` | Bloc de texte | `content`, `font_size`, `font_style`, `align`, `color` |
| `table` | Tableau avec en-têtes | `headers`, `rows`, `column_widths`, `column_aligns`, `striped_rows` |
| `image` | Image (fichier local) | `path`, `width`, `height`, `align` |
| `spacer` | Espace vertical | `height` |
| `section_title` | Titre de section coloré | `text`, `bg_color`, `text_color` |
| `key_value` | Paires label/valeur | `pairs`, `label_width`, `bold_labels` |
| `page_break` | Saut de page forcé | — |
| `separator` | Ligne horizontale | `color`, `thickness`, `width_percent` |
| `list` | Liste (puces, numéros, tirets) | `items`, `list_style`, `indent` |
| `box` | Conteneur bordé | `elements`, `border_color`, `bg_color`, `padding` |
| `columns` | Layout multi-colonnes | `columns[].width`, `columns[].elements`, `gap` |
| `qrcode` | QR code généré | `data`, `size`, `align` |
| `signature_block` | Bloc signatures | `signatures[].label`, `.name`, `.title` |

> 📖 Voir le [Guide d'utilisation complet](docs/guide.md) pour la documentation détaillée de chaque élément.

---

## ⚙️ Configuration du template

```python
ReportTemplate(
    # Page
    title="Mon Rapport",
    title_font_size=16,
    page=PageConfig(orientation="portrait", format="A4"),
    margins=MarginsConfig(top=15, bottom=15, left=15, right=15),

    # Font
    font=FontConfig(name="Helvetica", size=11),

    # Header & Footer
    header=HeaderConfig(
        lines=[HeaderLine(text="Ma Société", font_size=14, bold=True)],
        logo_left="logo.png",
        separator_line=True,
    ),
    footer=FooterConfig(
        left_text="Confidentiel",
        show_page_number=True,
        show_date=True,
    ),

    # Watermark
    watermark=WatermarkConfig(text="BROUILLON", color=[230, 230, 230]),

    # Variables (utilisables via {{key}} dans les textes)
    variables={"company": "KSB Tech", "ref": "RPT-001"},

    # Contenu
    elements=[...],
)
```

---

## 🛠 Développement

```bash
# Installation dev
pip install -e ".[dev]"

# Tests
python -m pytest -v

# Tests avec couverture
python -m pytest --cov=src/ksb_report --cov-report=term-missing

# Linting
ruff check src tests

# Formatage
ruff format src tests
```

---

## 📋 Roadmap

- [x] 13 types d'éléments de contenu
- [x] Variables dynamiques (`{{current_date}}`, custom)
- [x] Watermark configurable
- [x] Table avec alignement par colonne
- [x] QR Code, Signature Block
- [x] Templates pré-construits (Facture)
- [ ] Styles réutilisables (application par nom)
- [ ] Formules / calculs dans les templates
- [ ] Iterable data rendering (boucles JSON)
- [ ] Export HTML en plus du PDF

---

## 📄 License

[MIT](LICENSE) © [KINNOUME S. Borel](https://github.com/Kinbor1994)

---

## 🤝 Contributing

Les contributions sont les bienvenues ! Consultez [CONTRIBUTING.md](CONTRIBUTING.md) pour les guidelines.
