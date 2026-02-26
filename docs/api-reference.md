# API Reference — KSB-Report

## Base URL

```
http://localhost:8500
```

Port configurable via `--port` au lancement du serveur.

---

## Endpoints

### `GET /health`

Health check du serveur.

**Response** : `200 OK`

```json
{ "status": "ok" }
```

---

### `POST /api/reports/generate`

Génère un PDF et le retourne en téléchargement (`Content-Disposition: attachment`).

**Content-Type** : `application/json`

**Body** : objet `ReportTemplate` (voir [Guide](guide.md))

**Response** : `200 OK` — `application/pdf`

**Exemple** :

```bash
curl -X POST http://localhost:8500/api/reports/generate \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Mon Rapport",
    "elements": [
      {"type": "text", "content": "Hello World"},
      {"type": "table", "headers": ["A", "B"], "rows": [["1", "2"]]}
    ]
  }' \
  -o rapport.pdf
```

**Erreurs** :

| Code | Description |
|------|-------------|
| 422 | Validation error (JSON invalide) |
| 500 | Erreur de génération PDF |

---

### `POST /api/reports/preview`

Génère un PDF et le retourne en inline (`Content-Disposition: inline`), adapté pour l'affichage dans un navigateur ou iframe.

**Content-Type** : `application/json`

**Body** : identique à `/generate`

**Response** : `200 OK` — `application/pdf` (inline)

---

## Modèle de données

### `ReportTemplate`

```json
{
  "title": "string (optional)",
  "title_font_size": "float (default: 16)",
  "page": {
    "orientation": "portrait | landscape",
    "format": "A4 | A3 | Letter"
  },
  "margins": {
    "top": "float (default: 15)",
    "bottom": "float (default: 15)",
    "left": "float (default: 15)",
    "right": "float (default: 15)"
  },
  "font": {
    "name": "string (default: Helvetica)",
    "size": "float (default: 11)"
  },
  "header": "HeaderConfig | null",
  "footer": "FooterConfig | null",
  "watermark": "WatermarkConfig | null",
  "variables": "dict[string, string]",
  "elements": "ContentElement[]"
}
```

### Element types

| `type` | Modèle | Champs requis |
|--------|--------|---------------|
| `text` | `TextElement` | `content` |
| `table` | `TableElement` | `headers`, `rows` |
| `image` | `ImageElement` | `path` |
| `spacer` | `SpacerElement` | `height` |
| `section_title` | `SectionTitleElement` | `text` |
| `key_value` | `KeyValueElement` | `pairs` |
| `page_break` | `PageBreakElement` | — |
| `separator` | `SeparatorElement` | — |
| `list` | `ListElement` | `items` |
| `box` | `BoxElement` | `elements` |
| `columns` | `ColumnsElement` | `columns` |
| `qrcode` | `QRCodeElement` | `data` |
| `signature_block` | `SignatureBlockElement` | `signatures` |

Pour les détails complets de chaque élément, consultez le [Guide d'utilisation](guide.md#éléments-de-contenu).
