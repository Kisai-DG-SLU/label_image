"""
Tests for visualization utilities.
"""

import tempfile
from pathlib import Path
from unittest.mock import patch

import numpy as np
import pytest

from src.utils.visualization import (
    plot_clustering_results,
    plot_results,
    plot_training_history,
)


class TestPlotResults:
    """Test plot_results function."""

    # Mock plt.show() to prevent opening windows during tests
    @pytest.fixture(autouse=True)
    def mock_plt_show(self):
        with patch("matplotlib.pyplot.show"):
            yield

    def test_plot_results_with_metrics(self):
        """Test plot_results with basic metrics."""
        metrics = {
            "accuracy": 0.85,
            "precision": 0.82,
            "recall": 0.88,
            "f1_score": 0.85,
        }

        # Should not raise any exceptions
        plot_results(metrics)

    def test_plot_results_with_confusion_matrix(self):
        """Test plot_results with confusion matrix."""
        metrics = {
            "accuracy": 0.85,
            "confusion_matrix": np.array([[50, 5], [3, 42]]),
        }

        # Should not raise any exceptions
        plot_results(metrics)

    def test_plot_results_with_save_path(self):
        """Test plot_results with save_path."""
        metrics = {
            "accuracy": 0.85,
            "precision": 0.82,
            "recall": 0.88,
            "f1_score": 0.85,
        }

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmpfile:
            save_path = tmpfile.name
            plot_results(metrics, save_path=save_path)

            # Check file was created
            assert Path(save_path).exists()

            # Clean up
            Path(save_path).unlink()

    def test_plot_results_with_custom_title(self):
        """Test plot_results with custom title."""
        metrics = {"accuracy": 0.85}

        # Should not raise any exceptions
        plot_results(metrics, title="Custom Title")


class TestPlotClusteringResults:
    """Test plot_clustering_results function."""

    def test_plot_clustering_results_basic(self):
        """Test basic clustering plot."""
        # Create sample data
        np.random.seed(42)
        features = np.random.randn(100, 10)
        labels = np.random.randint(0, 3, 100)

        # Should not raise any exceptions
        plot_clustering_results(features, labels)

    def test_plot_clustering_results_with_reduced_features(self):
        """Test clustering plot with pre-reduced features."""
        np.random.seed(42)
        features = np.random.randn(100, 10)
        labels = np.random.randint(0, 3, 100)
        reduced_features = np.random.randn(100, 2)

        # Should not raise any exceptions
        plot_clustering_results(features, labels, reduced_features=reduced_features)

    def test_plot_clustering_results_with_save_path(self):
        """Test clustering plot with save_path."""
        np.random.seed(42)
        features = np.random.randn(50, 5)
        labels = np.random.randint(0, 2, 50)

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmpfile:
            save_path = tmpfile.name
            plot_clustering_results(features, labels, save_path=save_path)

            # Check file was created
            assert Path(save_path).exists()

            # Clean up
            Path(save_path).unlink()


class TestPlotTrainingHistory:
    """Test plot_training_history function."""

    def test_plot_training_history_basic(self):
        """Test basic training history plot."""
        history = {
            "loss": [0.5, 0.3, 0.2, 0.1],
            "accuracy": [0.7, 0.8, 0.85, 0.9],
        }

        # Should not raise any exceptions
        plot_training_history(history)

    def test_plot_training_history_with_validation(self):
        """Test training history plot with validation metrics."""
        history = {
            "loss": [0.5, 0.3, 0.2, 0.1],
            "val_loss": [0.6, 0.4, 0.3, 0.2],
            "accuracy": [0.7, 0.8, 0.85, 0.9],
            "val_accuracy": [0.65, 0.75, 0.8, 0.85],
        }

        # Should not raise any exceptions
        plot_training_history(history)

    def test_plot_training_history_with_save_path(self):
        """Test training history plot with save_path."""
        history = {
            "loss": [0.5, 0.3, 0.2, 0.1],
            "accuracy": [0.7, 0.8, 0.85, 0.9],
        }

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmpfile:
            save_path = tmpfile.name
            plot_training_history(history, save_path=save_path)

            # Check file was created
            assert Path(save_path).exists()

            # Clean up
            Path(save_path).unlink()

    def test_plot_training_history_empty(self):
        """Test training history plot with empty history."""
        history = {}

        # Should not raise any exceptions (plots empty axes)
        plot_training_history(history)


if __name__ == "__main__":
    pytest.main([__file__])
