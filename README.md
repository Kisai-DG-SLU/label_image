# BrainScanAI - Labellisation semi-supervisée pour détection de tumeurs cérébrales

## 📋 Description du projet

Projet de labellisation automatique et d'apprentissage semi-supervisé pour la détection de tumeurs cérébrales sur IRM. L'objectif est d'automatiser la détection de tumeurs cérébrales à partir d'IRM en utilisant l'apprentissage semi-supervisé pour pallier la rareté des labels experts.

## 🎯 Objectifs

1. **Maîtriser Red Hat OpenShift** pour l'entraînement et le déploiement de modèles ML
2. **Implémenter une solution ML complète** avec pipeline d'apprentissage semi-supervisé
3. **Produire les 3 livrables** demandés dans la description de mission

## 🚀 Fonctionnalités principales

- **Extraction de features** avec ResNet pré-entraîné
- **Clustering** (K-Means, DBSCAN) pour génération de labels faibles
- **Apprentissage semi-supervisé** avec fine-tuning sur labels experts
- **Pipeline MLops** sur Red Hat OpenShift avec Tekton et ArgoCD
- **Monitoring** complet avec Prometheus, Grafana et Jaeger

## 🏗️ Architecture

### Stack technique
- **Langage**: Python 3.11+ avec Pixi
- **ML Frameworks**: PyTorch 2.0+, TensorFlow 2.15+, scikit-learn
- **Orchestration**: Red Hat OpenShift 4.12+, Kubernetes
- **CI/CD**: GitHub Actions, Tekton Pipelines, ArgoCD
- **Monitoring**: Prometheus, Grafana, Jaeger, Loki
- **Documentation**: Sphinx, MkDocs, Jupyter Notebooks

### Structure du projet
```
brain-scan-ai/
├── src/                    # Code source
│   ├── data/              # Préprocessing des données
│   ├── features/          # Extraction de features
│   ├── models/           # Modèles ML
│   ├── training/         # Pipelines d'entraînement
│   ├── evaluation/       # Métriques et visualisation
│   ├── deployment/       # Déploiement OpenShift
│   └── utils/           # Utilitaires
├── tests/                # Tests unitaires et d'intégration
├── notebooks/           # Notebooks Jupyter
│   ├── 01_exploratory_analysis.ipynb
│   ├── 02_feature_extraction.ipynb
│   ├── 03_clustering_weak_labels.ipynb
│   ├── 04_semi_supervised_training.ipynb
│   └── 05_evaluation_visualization.ipynb
├── openshift/           # Configurations OpenShift
│   ├── templates/        # Templates OpenShift
│   ├── manifests/       # Manifests Kubernetes
│   ├── pipelines/       # Pipelines Tekton
│   └── monitoring/      # Monitoring et alerting
├── docs/                # Documentation
└── specs/              # Spécifications (dans IA & SPECS)
```

## ⚙️ Installation

### Prérequis
- Python 3.11+
- Pixi (gestionnaire d'environnements)
- Accès à un cluster Red Hat OpenShift 4.12+
- GPU recommandé pour l'entraînement

### Installation avec Pixi
```bash
# Cloner le repository
git clone <repository-url>
cd brain-scan-ai

# Installer les dépendances avec Pixi
pixi install

# Activer l'environnement
pixi shell

# Installer en mode développement
pixi run setup
```

### Installation manuelle
```bash
# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Sur Linux/Mac
# ou venv\Scripts\activate  # Sur Windows

# Installer les dépendances
pip install -e .[dev,openshift]
```

## 🚀 Utilisation

### Développement local
```bash
# Lancer les tests
pixi run test

# Linter le code
pixi run lint

# Formater le code
pixi run format

# Lancer les notebooks
pixi run notebook
```

### Entraînement du modèle
```bash
# Entraîner le modèle localement
pixi run train --config configs/train.yaml

# Évaluer le modèle
python src/evaluate.py --model checkpoints/best_model.pt
```

### Déploiement sur OpenShift
```bash
# Déployer sur OpenShift
oc apply -f openshift/manifests/

# Lancer le pipeline Tekton
tkn pipeline start brain-scan-ai-pipeline
```

## 📊 Livrables

1. **Notebook d'analyse exploratoire et clustering** : Extraction de features, PCA/t-SNE, K-Means
2. **Notebook de modélisation semi-supervisée** : Entraînement CNN, évaluation des métriques
3. **Support de présentation** : 15 slides incluant recommandations stratégiques et budgétaires

## 🔗 Intégration Red Hat OpenShift

Le projet est conçu pour une intégration complète avec Red Hat OpenShift :

- **Entraînement distribué** sur les GPU du cluster
- **Déploiement de modèles** via KServe ou Seldon Core
- **Pipeline MLops** avec Tekton pour l'entraînement automatique
- **Monitoring** avec Prometheus et Grafana
- **Auto-scaling** basé sur la charge de prédiction

## 📈 Métriques de performance

- **Précision modèle** : > 85% sur jeu de test
- **Temps d'inférence** : < 100ms par image
- **Couverture de tests** : > 70%
- **Disponibilité** : 99.9% sur OpenShift

## 🔄 CI/CD Pipeline

### Configuration GitHub Actions

Le projet utilise GitHub Actions pour l'intégration continue et le déploiement continu. Le workflow CI/CD est configuré dans `.github/workflows/ci.yml`.

#### Jobs du workflow CI

1. **Tests unitaires et linting** (`test`):
   - Exécute les tests avec pytest et mesure la couverture de code
   - Vérifie le linting avec Ruff et le formatage avec Black
   - Vérifie les types avec mypy
   - Génère un rapport de couverture uploadé sur Codecov

2. **Build et packaging** (`build`):
   - Construit le package Python avec `python -m build`
   - Upload les artefacts de build pour le déploiement

3. **Test des notebooks** (`notebook-test`):
   - Exécute tous les notebooks Jupyter pour vérifier qu'ils fonctionnent sans erreur

4. **Déploiement OpenShift** (`openshift-deploy`):
   - Déploie l'application sur Red Hat OpenShift (simulé pour l'instant)

5. **Création automatique de PR** (`auto-pr`):
   - Crée automatiquement une Pull Request de `develop` vers `main` après chaque push sur `develop`
   - Ajoute le label `automated-pr` pour identification

6. **Statut CI** (`ci`):
   - Agrège le statut de tous les jobs et génère un badge de statut

#### Règles de branche

- **Branche `main`** : Protégée avec les règles suivantes :
  - Requiert un review d'au moins 1 approbateur
  - Requiert que tous les checks CI passent
  - Requiert la résolution des conversations
  - Interdit les pushes directs (seules les PR sont autorisées)

- **Branche `develop`** : Protégée avec les règles suivantes :
  - Requiert que tous les checks CI passent
  - Permet les pushes directs pour les développeurs autorisés

#### Merge automatique

Le workflow `.github/workflows/auto-merge.yml` permet le merge automatique des PR avec le label `auto-merge` après :
- Tous les checks CI réussis
- Au moins 1 review approuvé
- Pas de conflits

#### Pré-commit hooks

Des hooks Git pré-commit sont configurés dans `.pre-commit-config.yaml` :
- Vérification du linting avec Ruff
- Formatage avec Black
- Vérification des types avec mypy
- Exécution automatique avant chaque commit

#### Configuration des dépendances

- **Pixi** : Gestionnaire de dépendances et d'environnements
- **PyTorch & TensorFlow** : Frameworks de deep learning
- **scikit-learn, pandas, numpy** : Bibliothèques de data science
- **Outils de qualité** : pytest, Ruff, Black, mypy, pre-commit

### Exécution locale

```bash
# Installer les dépendances
pixi install

# Installer le package en mode développement
pixi run setup

# Exécuter les tests
pixi run test

# Vérifier le linting et formatage
pixi run lint

# Formater le code
pixi run format
```

### Badges CI

[![CI Status](https://img.shields.io/badge/CI-passing-brightgreen)](https://github.com/damien-guesdon/brain-scan-ai/actions)
[![Code Coverage](https://img.shields.io/badge/coverage-40%25-yellow)](https://codecov.io/gh/damien-guesdon/brain-scan-ai)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🤝 Contribution

### Processus de développement
1. Créer une branche `feat/*` pour les nouvelles fonctionnalités
2. Implémenter les changements avec tests unitaires
3. Soumettre une Pull Request pour review
4. Valider les tests CI/CD
5. Merge après approbation

### Standards de code
- Formatage avec Black (ligne à 88 caractères)
- Linting avec Ruff
- Tests avec pytest (couverture > 70%)
- Documentation avec docstrings Google style

## 📄 Licence

MIT License - voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 📞 Contact

- **Auteur** : Damien Guesdon
- **Email** : damien@guesdon-brain.ai
- **Repository** : https://github.com/damien-guesdon/brain-scan-ai

## 🔗 Références

- [Documentation Red Hat OpenShift](https://docs.openshift.com)
- [Documentation PyTorch](https://pytorch.org/docs)
- [Documentation scikit-learn](https://scikit-learn.org)
- [Spécifications du projet](specs/)
-e 

## ✅ Configuration CI/CD Validée

La configuration CI/CD a été validée avec succès le 2026-02-09.
- ✅ Tous les workflows GitHub Actions passent
- ✅ Les règles de protection de branche sont configurées
- ✅ L'auto-merge fonctionne avec le label 'auto-merge'
- ✅ Les pré-commits vérifient le code avant chaque commit
- ✅ La couverture de code est mesurée et rapportée
- ✅ Les notebooks sont testés automatiquement
