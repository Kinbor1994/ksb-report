# Guide d'utilisation KSB-Report

Guide complet pour créer des rapports PDF avec KSB-Report.

---

## Table des matières

- [Architecture](#architecture)
- [Template JSON](#template-json)
- [Configuration](#configuration)
- [Éléments de contenu](#éléments-de-contenu)
- [Variables dynamiques](#variables-dynamiques)
- [Layouts avancés](#layouts-avancés)
- [Templates pré-construits](#templates-pré-construits)
- [API HTTP](#api-http)
- [CLI](#cli)

---

## Architecture

```
ReportTemplate (JSON/Pydantic)
        │
        ▼
   ReportEngine          ← Orchestration
        │
        ▼
    ReportFPDF           ← Rendu PDF (fpdf2)
        │
        ▼
   PDF bytes / fichier
```

Le workflow est simple :
1. Définir un `ReportTemplate` (en Python ou JSON)
2. Passer au `ReportEngine`
3. Recevoir le PDF en bytes ou fichier

---

## Template JSON

Un template est un objet JSON avec cette structure :

```json
{
  "title": "Mon Rapport",
  "title_font_size": 16,
  "page": { "orientation": "portrait", "format": "A4" },
  "margins": { "top": 15, "bottom": 15, "left": 15, "right": 15 },
  "font": { "name": "Helvetica", "size": 11 },
  "header": { ... },
  "footer": { ... },
  "watermark": { ... },
  "variables": { "key": "value" },
  "elements": [ ... ]
}
```

Seul `elements` est obligatoire. Tout le reste a des valeurs par défaut sensées.

---

## Configuration

### Page (`page`)

| Paramètre | Type | Défaut | Description |
|-----------|------|--------|-------------|
| `orientation` | `"portrait"` \| `"landscape"` | `"portrait"` | Orientation de la page |
| `format` | `"A4"` \| `"A3"` \| `"Letter"` | `"A4"` | Format papier |

### Marges (`margins`)

| Paramètre | Type | Défaut | Description |
|-----------|------|--------|-------------|
| `top` | float | 15 | Marge haute (mm) |
| `bottom` | float | 15 | Marge basse (mm) |
| `left` | float | 15 | Marge gauche (mm) |
| `right` | float | 15 | Marge droite (mm) |

### Police (`font`)

| Paramètre | Type | Défaut | Description |
|-----------|------|--------|-------------|
| `name` | string | `"Helvetica"` | Nom de la police |
| `size` | float | 11 | Taille par défaut (pt) |

### En-tête (`header`)

```json
{
  "header": {
    "enabled": true,
    "lines": [
      { "text": "Ma Société", "font_size": 16, "bold": true, "align": "C" },
      { "text": "Département IT", "font_size": 10, "italic": true }
    ],
    "logo_left": "path/to/logo.png",
    "logo_right": "path/to/logo2.png",
    "logo_width": 25,
    "logo_height": 25,
    "separator_line": true,
    "color_bar": {
      "color": [41, 128, 185],
      "height": 3,
      "position": "top"
    }
  }
}
```

### Pied de page (`footer`)

```json
{
  "footer": {
    "left_text": "Confidentiel",
    "center_text": "",
    "show_page_number": true,
    "show_date": true,
    "font_size": 8
  }
}
```

### Filigrane (`watermark`)

```json
{
  "watermark": {
    "text": "BROUILLON",
    "color": [230, 230, 230],
    "font_size": 60,
    "opacity": 0.3
  }
}
```

---

## Éléments de contenu

Chaque élément est un objet dans le tableau `elements` avec un champ `type` discriminant.

### `text` — Bloc de texte

```json
{
  "type": "text",
  "content": "Lorem ipsum dolor sit amet.",
  "font_size": 12,
  "font_style": "B",
  "align": "L",
  "color": [0, 0, 0]
}
```

| Paramètre | Type | Défaut | Description |
|-----------|------|--------|-------------|
| `content` | string | **requis** | Texte à afficher (supporte `{{variables}}`) |
| `font_size` | float | 11 | Taille de police |
| `font_style` | `""` \| `"B"` \| `"I"` \| `"BI"` | `""` | Style (Bold, Italic) |
| `align` | `"L"` \| `"C"` \| `"R"` | `"L"` | Alignement |
| `color` | `[r, g, b]` | `[0, 0, 0]` | Couleur du texte |

---

### `table` — Tableau

```json
{
  "type": "table",
  "headers": ["Nom", "Qté", "Prix"],
  "rows": [
    ["Widget A", "2", "15 000 FCFA"],
    ["Service B", "1", "50 000 FCFA"]
  ],
  "column_widths": [50, 20, 30],
  "column_aligns": ["L", "C", "R"],
  "header_bg_color": [41, 128, 185],
  "header_text_color": [255, 255, 255],
  "striped_rows": true
}
```

| Paramètre | Type | Défaut | Description |
|-----------|------|--------|-------------|
| `headers` | list[string] | **requis** | En-têtes de colonnes |
| `rows` | list[list[string]] | **requis** | Lignes de données |
| `column_widths` | list[float] \| null | auto | Largeurs en % (normalisées) |
| `column_aligns` | list[string] \| null | `["L", ...]` | Alignement par colonne |
| `column_types` | list[string] \| null | null | Types (`"text"`, `"image"`) |
| `header_bg_color` | `[r,g,b]` | `[41,128,185]` | Fond des en-têtes |
| `header_text_color` | `[r,g,b]` | `[255,255,255]` | Texte des en-têtes |
| `striped_rows` | bool | true | Alternance de couleurs |
| `max_rows_per_page` | int \| null | null | Max lignes avant saut |
| `font_size` | float | 10 | Taille police cellules |
| `header_font_size` | float | 10 | Taille police en-têtes |

---

### `image` — Image

```json
{
  "type": "image",
  "path": "/path/to/image.png",
  "width": 80,
  "height": 60,
  "align": "C"
}
```

---

### `spacer` — Espace vertical

```json
{ "type": "spacer", "height": 10 }
```

---

### `section_title` — Titre de section

```json
{
  "type": "section_title",
  "text": "I. INTRODUCTION",
  "bg_color": [41, 128, 185],
  "text_color": [255, 255, 255],
  "font_size": 12
}
```

---

### `key_value` — Paires label/valeur

```json
{
  "type": "key_value",
  "pairs": [
    ["Référence", "RPT-001"],
    ["Date", "{{current_date}}"],
    ["Auteur", "{{author}}"]
  ],
  "label_width": 35,
  "bold_labels": true,
  "font_size": 11
}
```

---

### `page_break` — Saut de page

```json
{ "type": "page_break" }
```

---

### `separator` — Ligne horizontale

```json
{
  "type": "separator",
  "color": [200, 200, 200],
  "thickness": 0.5,
  "width_percent": 100,
  "margin_top": 3,
  "margin_bottom": 3
}
```

---

### `list` — Liste

```json
{
  "type": "list",
  "items": ["Premier point", "Deuxième point", "Troisième point"],
  "list_style": "bullet",
  "font_size": 11,
  "indent": 10,
  "spacing": 2
}
```

| `list_style` | Rendu |
|-------------|-------|
| `"bullet"` | • Premier point |
| `"numbered"` | 1. Premier point |
| `"dash"` | – Premier point |

---

### `box` — Conteneur bordé

```json
{
  "type": "box",
  "border_color": [231, 76, 60],
  "bg_color": [253, 237, 236],
  "padding": 6,
  "corner_radius": 3,
  "elements": [
    { "type": "text", "content": "Attention !", "font_style": "B" }
  ]
}
```

Les `elements` à l'intérieur du box supportent tous les types d'éléments.

---

### `columns` — Layout multi-colonnes

```json
{
  "type": "columns",
  "gap": 10,
  "columns": [
    {
      "width": 50,
      "elements": [
        { "type": "text", "content": "Colonne gauche" }
      ]
    },
    {
      "width": 50,
      "elements": [
        { "type": "text", "content": "Colonne droite" }
      ]
    }
  ]
}
```

- `width` : pourcentage relatif (normalisé)
- Supporte 2, 3 ou plus de colonnes
- Chaque colonne contient ses propres éléments

---

### `qrcode` — QR Code

```json
{
  "type": "qrcode",
  "data": "https://example.com",
  "size": 30,
  "align": "C"
}
```

| Paramètre | Type | Défaut | Description |
|-----------|------|--------|-------------|
| `data` | string | **requis** | Contenu du QR code |
| `size` | float | 30 | Taille en mm |
| `align` | `"L"` \| `"C"` \| `"R"` | `"C"` | Alignement horizontal |

Nécessite la dépendance `qrcode[pil]` (incluse par défaut).

---

### `signature_block` — Bloc de signatures

```json
{
  "type": "signature_block",
  "signatures": [
    {
      "label": "Le Directeur",
      "name": "M. DUPONT",
      "title": "Directeur Général"
    },
    {
      "label": "Le Chef de Projet",
      "name": "Mme. MARTIN",
      "title": "PM"
    }
  ],
  "line_width": 40,
  "spacing": 20
}
```

Les signatures sont réparties horizontalement sur la page.

---

## Variables dynamiques

Utilisez `{{nom_variable}}` dans n'importe quel champ texte :

```json
{
  "variables": {
    "company": "Ma Société",
    "ref": "RPT-2026-001"
  },
  "elements": [
    { "type": "text", "content": "Rapport de {{company}} — Réf: {{ref}}" }
  ]
}
```

### Variables built-in

| Variable | Valeur |
|----------|--------|
| `{{current_date}}` | Date du jour (DD/MM/YYYY) |
| `{{current_time}}` | Heure actuelle (HH:MM) |
| `{{year}}` | Année en cours |
| `{{month}}` | Mois en cours (01-12) |
| `{{day}}` | Jour du mois |

---

## Templates pré-construits

### Facture

```python
from ksb_report.templates import invoice_template

template = invoice_template(
    company_name="Ma Société",
    company_address="Cotonou, Bénin",
    company_phone="+229 97 00 00 00",
    invoice_number="2026-001",
    client_name="Jean Dupont",
    client_address="Paris, France",
    items=[
        {"description": "Widget A", "quantity": 2, "unit_price": 15.00},
        {"description": "Service B", "quantity": 1, "unit_price": 50.00},
    ],
    tax_rate=0.18,
    currency="FCFA",
)
```

---

## API HTTP

### Démarrer le serveur

```bash
ksb-report serve --port 8500 --host 0.0.0.0
```

### Endpoints

#### `POST /api/reports/generate`

Génère un PDF et le retourne en téléchargement.

```bash
curl -X POST http://localhost:8500/api/reports/generate \
  -H "Content-Type: application/json" \
  -d @template.json \
  -o rapport.pdf
```

#### `POST /api/reports/preview`

Retourne le PDF en inline (pour affichage navigateur).

```bash
curl -X POST http://localhost:8500/api/reports/preview \
  -H "Content-Type: application/json" \
  -d @template.json \
  -o preview.pdf
```

#### `GET /health`

Vérification de santé du serveur.

```bash
curl http://localhost:8500/health
# → {"status": "ok"}
```

---

## CLI

```bash
# Générer un PDF depuis un fichier JSON
ksb-report generate template.json -o output.pdf

# Lancer le serveur API
ksb-report serve --port 8500

# Aide
ksb-report --help
```
