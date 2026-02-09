# Makefile for BrainScanAI Project

.PHONY: help setup test lint format clean install dev docs openshift

help:
	@echo "BrainScanAI - Makefile"
	@echo "========================"
	@echo ""
	@echo "Available targets:"
	@echo "  setup     - Install dependencies and setup environment"
	@echo "  install   - Install production dependencies"
	@echo "  dev       - Install development dependencies"
	@echo "  test      - Run tests with coverage"
	@echo "  lint      - Run linters (ruff, black, mypy)"
	@echo "  format    - Format code with black and ruff"
	@echo "  notebook  - Start Jupyter notebook server"
	@echo "  train     - Train the model"
	@echo "  evaluate  - Evaluate the model"
	@echo "  docs      - Build documentation"
	@echo "  openshift - Install OpenShift dependencies"
	@echo "  clean     - Clean build artifacts"
	@echo "  help      - Show this help"

setup: install dev
	@echo "Environment setup complete"

install:
	@pixi install
	@echo "Production dependencies installed"

dev:
	@pixi install --feature dev
	@echo "Development dependencies installed"

openshift:
	@pixi install --feature openshift
	@echo "OpenShift dependencies installed"

test:
	@pixi run test

lint:
	@pixi run lint

format:
	@pixi run format

notebook:
	@pixi run notebook

train:
	@pixi run train

serve:
	@pixi run serve

docs:
	@pixi install --feature docs
	@sphinx-build docs/source docs/build

clean:
	@rm -rf build/
	@rm -rf dist/
	@rm -rf *.egg-info
	@rm -rf .pytest_cache/
	@rm -rf .mypy_cache/
	@rm -rf .ruff_cache/
	@rm -rf htmlcov/
	@rm -rf .coverage
	@rm -rf docs/build/
	@rm -rf mlruns/
	@rm -rf .ipynb_checkpoints/
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete
	@find . -type f -name "*.pyo" -delete
	@find . -type f -name "*.pyd" -delete
	@echo "Cleaned build artifacts"

# OpenShift targets
openshift-login:
	@echo "Logging into OpenShift cluster..."
	# oc login --token=your-token --server=your-server

openshift-create-ns:
	@echo "Creating OpenShift namespace..."
	# oc create namespace brain-scan-ai

openshift-deploy:
	@echo "Deploying to OpenShift..."
	# oc apply -f openshift/manifests/

openshift-pipeline:
	@echo "Starting Tekton pipeline..."
	# tkn pipeline start brain-scan-ai-pipeline

# Data preparation
download-data:
	@echo "Downloading datasets..."
	# python src/data/download.py

preprocess:
	@echo "Preprocessing data..."
	# python src/data/preprocess.py

# Model training
train-baseline:
	@echo "Training baseline model..."
	# python src/train.py --config configs/baseline.yaml

train-semisupervised:
	@echo "Training semi-supervised model..."
	# python src/train.py --config configs/semisupervised.yaml

# Evaluation
evaluate:
	@echo "Evaluating model..."
	# python src/evaluate.py --model checkpoints/best_model.pt

visualize:
	@echo "Generating visualizations..."
	# python src/visualize.py --results results/metrics.json

# Notebooks
convert-notebooks:
	@echo "Converting notebooks to HTML..."
	# jupyter nbconvert --to html notebooks/*.ipynb --output-dir docs/notebooks/

# Docker
docker-build:
	@echo "Building Docker image..."
	# docker build -t brain-scan-ai:latest .

docker-run:
	@echo "Running Docker container..."
	# docker run -p 8080:8080 brain-scan-ai:latest

# Utility
update-deps:
	@pixi update
	@echo "Dependencies updated"

check-env:
	@echo "Checking environment..."
	@pixi info
	@python --version
	@python -c "import torch; print(f'PyTorch: {torch.__version__}')"
	@python -c "import tensorflow as tf; print(f'TensorFlow: {tf.__version__}')"
	@echo "Environment check complete"

# Default target
.DEFAULT_GOAL := help
