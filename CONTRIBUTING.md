# Contributing to KSB-Report

Merci de votre intérêt pour contribuer à KSB-Report ! 🎉

## 🚀 Setup de développement

```bash
# Cloner le dépôt
git clone https://github.com/Kinbor1994/ksb-report.git
cd ksb-report

# Installer en mode dev
pip install -e ".[dev]"

# Vérifier que les tests passent
python -m pytest -v
```

## 📋 Workflow de contribution

1. **Fork** le repo et créez une **branche** depuis `main`
   ```bash
   git checkout -b feat/my-feature
   ```

2. **Écrivez votre code** en suivant les conventions ci-dessous

3. **Ajoutez des tests** pour toute nouvelle fonctionnalité

4. **Vérifiez que tout passe** :
   ```bash
   python -m pytest -v
   ruff check src tests
   ruff format src tests
   ```

5. **Committez** avec un message clair ([Conventional Commits](https://www.conventionalcommits.org/)) :
   ```
   feat: add barcode element
   fix: column layout overflow on page break
   docs: update guide with new examples
   ```

6. **Ouvrez une Pull Request** vers `main`

## 🏗 Architecture du projet

```
src/ksb_report/
├── __init__.py      # API publique, exports
├── schemas.py       # Modèles Pydantic (JSON contract)
├── pdf.py           # Moteur de rendu FPDF2
├── engine.py        # Orchestration (template → PDF)
├── api.py           # Endpoints FastAPI
├── cli.py           # Interface CLI
├── fonts/           # Polices embarquées
└── templates/       # Templates pré-construits
```

## 📏 Conventions de code

- **Python 3.10+** — utilisation des type hints modernes (`X | None`, `list[str]`)
- **Formatage** : `ruff format`
- **Linting** : `ruff check`
- **Tests** : `pytest` — chaque nouvel élément doit avoir des tests dans `test_schemas.py` et `test_engine.py`
- **Docstrings** : obligatoires pour les classes et méthodes publiques

## 🧪 Tests

```bash
# Tous les tests
python -m pytest -v

# Avec couverture
python -m pytest --cov=src/ksb_report --cov-report=term-missing

# Un seul fichier
python -m pytest tests/test_engine.py -v
```

## 🐛 Signaler un bug

Ouvrez une [issue](https://github.com/Kinbor1994/ksb-report/issues) avec :
- Description du problème
- Template JSON minimal pour reproduire
- Version de Python et de `ksb-report`
- PDF résultant (si applicable)

## 💡 Proposer une fonctionnalité

Ouvrez une [issue](https://github.com/Kinbor1994/ksb-report/issues) avec le label `enhancement` et décrivez :
- Le use case
- Le comportement attendu
- Un exemple JSON si possible

## 📄 License

En contribuant, vous acceptez que vos contributions soient sous licence [MIT](LICENSE).
