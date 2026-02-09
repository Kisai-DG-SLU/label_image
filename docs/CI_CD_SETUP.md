# Configuration CI/CD - BrainScanAI

Ce document décrit la configuration complète du pipeline CI/CD pour le projet BrainScanAI.

## 📋 Vue d'ensemble

Le pipeline CI/CD est configuré avec GitHub Actions et comprend les fonctionnalités suivantes :
- Tests unitaires avec couverture de code
- Linting et formatage automatique
- Build et packaging
- Tests des notebooks Jupyter
- Déploiement simulé sur OpenShift
- Création automatique de PR
- Merge automatique avec labels
- Protection des branches

## 🛠️ Configuration GitHub Actions

### Workflow principal : `.github/workflows/ci.yml`

Le workflow principal s'exécute sur :
- Push sur les branches `main` et `develop`
- Pull requests vers `main` et `develop`
- Changements dans les fichiers source (`src/`, `tests/`, `notebooks/`, fichiers de configuration)

### Jobs du workflow

#### 1. Tests unitaires et linting (`test`)
```yaml
- name: Setup Pixi
  uses: prefix-dev/setup-pixi@v0.5.2
  with:
    pixi-version: 'v0.32.0'

- name: Install dependencies
  run: pixi install

- name: Setup package in development mode
  run: pixi run setup

- name: Run linting and formatting checks
  run: pixi run lint

- name: Run tests with coverage
  run: pixi run test

- name: Upload coverage reports
  uses: codecov/codecov-action@v4
```

#### 2. Build et packaging (`build`)
- Build du package Python avec `python -m build`
- Upload des artefacts pour déploiement

#### 3. Test des notebooks (`notebook-test`)
- Exécution de tous les notebooks avec `nbconvert --execute`
- Vérification qu'ils s'exécutent sans erreur

#### 4. Déploiement OpenShift (`openshift-deploy`)
- Simulation du déploiement sur Red Hat OpenShift
- S'exécute uniquement sur la branche `main`

#### 5. Création automatique de PR (`auto-pr`)
- Crée automatiquement une PR de `develop` vers `main` après chaque push sur `develop`
- Utilise l'action `peter-evans/create-pull-request@v6`
- Ajoute le label `automated-pr`

#### 6. Statut CI (`ci`)
- Agrège le statut de tous les jobs
- Génère un badge de statut CI

## 🔒 Protection des branches

### Configuration via GitHub CLI

Les règles de protection sont configurées avec les fichiers JSON suivants :

#### `branch_protection_main.json`
```json
{
  "required_status_checks": {
    "strict": true,
    "contexts": ["ci"]
  },
  "enforce_admins": true,
  "required_pull_request_reviews": {
    "required_approving_review_count": 1
  },
  "restrictions": null,
  "required_conversation_resolution": true
}
```

#### `branch_protection_develop.json`
```json
{
  "required_status_checks": {
    "strict": true,
    "contexts": ["ci"]
  },
  "enforce_admins": false,
  "required_pull_request_reviews": null,
  "restrictions": null,
  "required_conversation_resolution": false
}
```

### Application des règles

```bash
# Protection de la branche main
gh api repos/:owner/:repo/branches/main/protection \
  --input branch_protection_main.json

# Protection de la branche develop
gh api repos/:owner/:repo/branches/develop/protection \
  --input branch_protection_develop.json
```

## 🤖 Merge automatique

### Configuration : `.github/auto-merge.yml`
```yaml
# Configuration pour le merge automatique
autoMerge:
  enabled: true
  mergeMethod: squash
  deleteBranchAfterMerge: true
  requiredLabels:
    - auto-merge
  blockingLabels:
    - do-not-merge
```

### Workflow : `.github/workflows/auto-merge.yml`
- S'exécute sur les pull requests
- Vérifie les conditions de merge automatique
- Merge automatiquement les PR avec le label `auto-merge`

## 🧪 Pré-commit hooks

### Configuration : `.pre-commit-config.yaml`
```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.5.0
    hooks:
      - id: mypy
        additional_dependencies: [types-all]
```

### Script local : `.githooks/pre-commit`
```bash
#!/bin/bash
pixi run lint
if [ $? -ne 0 ]; then
  echo "Linting failed. Please fix the issues before committing."
  exit 1
fi
```

## 📦 Gestion des dépendances

### Pixi (`pixi.toml`)
```toml
[workspace]
name = "brain-scan-ai"
version = "0.1.0"
description = "Labellisation semi-supervisée pour la détection de tumeurs cérébrales sur IRM avec intégration Red Hat OpenShift"
authors = ["Damien GUESDON <kisai.dg.slu@gmail.com>"]
channels = ["conda-forge"]
platforms = ["osx-64", "linux-64"]

[tasks]
setup = "python -m pip install -e '.[dev]'"
test = "pytest tests/ -v --cov=src --cov-report=term-missing --cov-report=html"
lint = "ruff check src/ tests/ && black --check src/ tests/ && mypy src/"
format = "black src/ tests/ && ruff check --fix src/ tests/"
notebook = "jupyter notebook notebooks/"
train = "python src/train.py"
serve = "python src/serve.py"

[dependencies]
python = "3.11.*"
pip = "*"
scikit-learn = ">=1.3.2"
pandas = ">=2.1.4"
numpy = ">=1.26.0"
matplotlib = ">=3.8.0"
seaborn = ">=0.13.0"
jupyter = ">=1.0.0"
notebook = ">=7.0.6"
python-dotenv = ">=1.0.0"
typer = ">=0.9.0"
rich = ">=13.7.0"

[pypi-dependencies]
torch = ">=2.0.0"
torchvision = ">=0.15.0"
tensorflow = ">=2.15.0"

[feature.dev.dependencies]
pytest = ">=7.4.0"
pytest-cov = ">=4.1.0"
ruff = ">=0.1.0"
black = ">=23.0.0"
mypy = ">=1.5.0"
pre-commit = ">=3.5.0"

[feature.ml.dependencies]
mlflow = ">=2.8.0"
hydra-core = ">=1.3.0"
pydantic = ">=2.0.0"
opencv-python = ">=4.8.0"
plotly = ">=5.15.0"
```

### PyProject (`pyproject.toml`)
- Configuration du package Python avec setuptools
- Dépendances principales et optionnelles
- Configuration des outils de qualité (Black, Ruff, Mypy, pytest)

## 🧪 Tests et qualité

### Configuration pytest (`pytest.ini`)
```ini
[pytest]
testpaths = tests
python_files = test_*.py
addopts = 
    -v
    --cov=src
    --cov-report=term-missing
    --cov-report=html
    --cov-fail-under=70
filterwarnings = 
    ignore::UserWarning
    ignore::DeprecationWarning
```

### Couverture de code
- Seuil minimum : 70%
- Rapport HTML généré dans `htmlcov/`
- Rapport XML pour Codecov

## 🚀 Workflow de développement

### 1. Créer une branche de fonctionnalité
```bash
git checkout -b feat/nouvelle-fonctionnalite
```

### 2. Développer et tester localement
```bash
# Installer les dépendances
pixi install

# Installer le package en mode développement
pixi run setup

# Exécuter les tests
pixi run test

# Vérifier le linting
pixi run lint

# Formater le code
pixi run format
```

### 3. Commiter avec les hooks pré-commit
```bash
git add .
git commit -m "feat: ajout nouvelle fonctionnalité"
# Les hooks pré-commit s'exécutent automatiquement
```

### 4. Pousser vers GitHub
```bash
git push origin feat/nouvelle-fonctionnalite
```

### 5. Créer une Pull Request
- La PR sera automatiquement vérifiée par le workflow CI
- Les tests, linting et coverage seront exécutés
- Un review est requis pour merge dans `main`

### 6. Merge automatique
- Ajouter le label `auto-merge` à la PR
- Le workflow auto-merge vérifiera les conditions
- Merge automatique après approbation et réussite des tests

## 🔧 Dépannage

### Problèmes courants

#### Erreur "ModuleNotFoundError: No module named 'src'"
**Solution** : Exécuter `pixi run setup` pour installer le package en mode développement.

#### Erreur de linting
**Solution** : Exécuter `pixi run format` pour formater automatiquement le code, puis `pixi run lint` pour vérifier.

#### Erreur de coverage insuffisant
**Solution** : Ajouter des tests pour les fonctions non couvertes. Le seuil minimum est de 70%.

#### Erreur avec pixi.lock
**Solution** : Supprimer `pixi.lock` et réexécuter `pixi install` pour régénérer le fichier.

### Commandes utiles

```bash
# Nettoyer l'environnement pixi
pixi clean

# Régénérer le lockfile
rm pixi.lock && pixi install

# Exécuter un notebook spécifique
pixi run python -m nbconvert --execute notebooks/01_exploratory_analysis.ipynb

# Voir la couverture de code
open htmlcov/index.html
```

## 📊 Monitoring CI

### Badges
- **Statut CI** : [![CI Status](https://img.shields.io/badge/CI-passing-brightgreen)](https://github.com/damien-guesdon/brain-scan-ai/actions)
- **Couverture de code** : [![Code Coverage](https://img.shields.io/badge/coverage-40%25-yellow)](https://codecov.io/gh/damien-guesdon/brain-scan-ai)

### Dashboard GitHub Actions
- Accéder à https://github.com/damien-guesdon/brain-scan-ai/actions
- Voir l'historique des exécutions
- Télécharger les artefacts de build
- Consulter les logs détaillés

## 🔄 Mise à jour de la configuration

Pour mettre à jour la configuration CI/CD :

1. Modifier les fichiers dans `.github/workflows/`
2. Tester localement avec `act` (simulateur GitHub Actions)
3. Pousser les changements sur `develop`
4. Vérifier que le workflow CI passe
5. Merge dans `main` via PR

## 📚 Références

- [Documentation GitHub Actions](https://docs.github.com/en/actions)
- [Documentation Pixi](https://pixi.sh/)
- [Documentation pre-commit](https://pre-commit.com/)
- [Documentation pytest](https://docs.pytest.org/)
- [Documentation Codecov](https://docs.codecov.com/)

