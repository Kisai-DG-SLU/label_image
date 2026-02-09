"""
Tests for model monitoring module.
"""

import tempfile
from pathlib import Path
from unittest.mock import patch

import numpy as np
import pandas as pd
import pytest

from src.model.monitoring import ModelMonitor


class TestModelMonitor:
    """Test ModelMonitor class."""

    # Mock plt.show() to prevent opening windows during tests
    @pytest.fixture(autouse=True)
    def mock_plt_show(self):
        with patch("matplotlib.pyplot.show"):
            yield

    def test_init(self):
        """Test ModelMonitor initialization."""
        monitor = ModelMonitor()
        assert monitor.model_name == "brain-scan-ai"
        assert monitor.metrics_history == []
        assert monitor.predictions == []
        assert monitor.labels == []

    def test_init_with_custom_name(self):
        """Test ModelMonitor initialization with custom name."""
        monitor = ModelMonitor(model_name="custom-model")
        assert monitor.model_name == "custom-model"

    def test_add_prediction_binary(self):
        """Test adding binary predictions."""
        monitor = ModelMonitor()

        # Add binary predictions (single probability)
        monitor.add_prediction(np.array([0.7]), 1)
        monitor.add_prediction(np.array([0.3]), 0)
        monitor.add_prediction(np.array([0.9]), 1)

        assert len(monitor.predictions) == 3
        assert len(monitor.labels) == 3
        assert monitor.predictions[0].shape == (1,)
        assert monitor.labels == [1, 0, 1]

    def test_add_prediction_multiclass(self):
        """Test adding multiclass predictions."""
        monitor = ModelMonitor()

        # Add multiclass predictions (probability distribution)
        monitor.add_prediction(np.array([0.1, 0.8, 0.1]), 1)
        monitor.add_prediction(np.array([0.7, 0.2, 0.1]), 0)

        assert len(monitor.predictions) == 2
        assert monitor.predictions[0].shape == (3,)
        assert monitor.labels == [1, 0]

    def test_calculate_metrics_empty(self):
        """Test calculate_metrics with no predictions."""
        monitor = ModelMonitor()
        metrics = monitor.calculate_metrics()
        assert metrics == {}

    def test_calculate_metrics_binary(self):
        """Test calculate_metrics with binary predictions."""
        monitor = ModelMonitor()

        # Add some predictions with perfect accuracy
        monitor.add_prediction(np.array([0.9]), 1)  # Prediction: 1, Label: 1
        monitor.add_prediction(np.array([0.8]), 1)  # Prediction: 1, Label: 1
        monitor.add_prediction(np.array([0.2]), 0)  # Prediction: 0, Label: 0
        monitor.add_prediction(np.array([0.1]), 0)  # Prediction: 0, Label: 0

        metrics = monitor.calculate_metrics()

        assert "accuracy" in metrics
        assert "precision" in metrics
        assert "recall" in metrics
        assert "f1_score" in metrics
        assert "n_samples" in metrics
        assert metrics["n_samples"] == 4
        assert metrics["accuracy"] == 1.0  # Perfect predictions

        # Check history was updated
        assert len(monitor.metrics_history) == 1
        assert monitor.metrics_history[0] == metrics

    def test_calculate_metrics_multiclass(self):
        """Test calculate_metrics with multiclass predictions."""
        monitor = ModelMonitor()

        # Add multiclass predictions (3 classes)
        monitor.add_prediction(
            np.array([0.1, 0.8, 0.1]), 1
        )  # Prediction: class 1, Label: 1
        monitor.add_prediction(
            np.array([0.7, 0.2, 0.1]), 0
        )  # Prediction: class 0, Label: 0
        monitor.add_prediction(
            np.array([0.1, 0.1, 0.8]), 2
        )  # Prediction: class 2, Label: 2

        metrics = monitor.calculate_metrics()

        assert "accuracy" in metrics
        assert "precision" in metrics
        assert "recall" in metrics
        assert "f1_score" in metrics
        assert "n_samples" in metrics
        assert metrics["n_samples"] == 3
        assert metrics["accuracy"] == 1.0  # Perfect predictions

    def test_calculate_metrics_multiple_calls(self):
        """Test calculate_metrics called multiple times."""
        monitor = ModelMonitor()

        # First batch
        monitor.add_prediction(np.array([0.9]), 1)
        monitor.add_prediction(np.array([0.2]), 0)
        metrics1 = monitor.calculate_metrics()

        # Second batch
        monitor.add_prediction(np.array([0.8]), 1)
        monitor.add_prediction(np.array([0.3]), 0)
        metrics2 = monitor.calculate_metrics()

        assert len(monitor.metrics_history) == 2
        assert monitor.metrics_history[0] == metrics1
        assert monitor.metrics_history[1] == metrics2
        assert metrics2["n_samples"] == 4

    def test_plot_confusion_matrix_empty(self):
        """Test plot_confusion_matrix with no predictions."""
        monitor = ModelMonitor()
        # Should not raise any exceptions
        monitor.plot_confusion_matrix()

    def test_plot_confusion_matrix_with_predictions(self):
        """Test plot_confusion_matrix with predictions."""
        monitor = ModelMonitor()

        # Add some predictions
        monitor.add_prediction(np.array([0.9]), 1)
        monitor.add_prediction(np.array([0.2]), 0)
        monitor.add_prediction(np.array([0.8]), 1)
        monitor.add_prediction(np.array([0.3]), 0)

        # Calculate metrics first
        monitor.calculate_metrics()

        # Should not raise any exceptions
        monitor.plot_confusion_matrix()

    def test_plot_confusion_matrix_with_save_path(self):
        """Test plot_confusion_matrix with save_path."""
        monitor = ModelMonitor()

        # Add some predictions
        monitor.add_prediction(np.array([0.9]), 1)
        monitor.add_prediction(np.array([0.2]), 0)

        monitor.calculate_metrics()

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmpfile:
            save_path = tmpfile.name
            monitor.plot_confusion_matrix(save_path=save_path)

            # Check file was created
            assert Path(save_path).exists()

            # Clean up
            Path(save_path).unlink()

    def test_plot_roc_curve_empty(self):
        """Test plot_roc_curve with no predictions."""
        monitor = ModelMonitor()
        # Should not raise any exceptions
        monitor.plot_roc_curve()

    def test_plot_roc_curve_with_predictions(self):
        """Test plot_roc_curve with predictions."""
        monitor = ModelMonitor()

        # Add some predictions
        monitor.add_prediction(np.array([0.9]), 1)
        monitor.add_prediction(np.array([0.2]), 0)
        monitor.add_prediction(np.array([0.8]), 1)
        monitor.add_prediction(np.array([0.3]), 0)

        # Should not raise any exceptions
        monitor.plot_roc_curve()

    def test_plot_roc_curve_with_save_path(self):
        """Test plot_roc_curve with save_path."""
        monitor = ModelMonitor()

        # Add some predictions
        monitor.add_prediction(np.array([0.9]), 1)
        monitor.add_prediction(np.array([0.2]), 0)

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmpfile:
            save_path = tmpfile.name
            monitor.plot_roc_curve(save_path=save_path)

            # Check file was created
            assert Path(save_path).exists()

            # Clean up
            Path(save_path).unlink()

    def test_get_history_df_empty(self):
        """Test get_history_df with no history."""
        monitor = ModelMonitor()
        df = monitor.get_history_df()

        assert isinstance(df, pd.DataFrame)
        assert len(df) == 0

    def test_get_history_df_with_history(self):
        """Test get_history_df with history."""
        monitor = ModelMonitor()

        # Add predictions and calculate metrics twice
        monitor.add_prediction(np.array([0.9]), 1)
        monitor.add_prediction(np.array([0.2]), 0)
        monitor.calculate_metrics()

        monitor.add_prediction(np.array([0.8]), 1)
        monitor.add_prediction(np.array([0.3]), 0)
        monitor.calculate_metrics()

        df = monitor.get_history_df()

        assert isinstance(df, pd.DataFrame)
        assert len(df) == 2
        assert "accuracy" in df.columns
        assert "precision" in df.columns
        assert "recall" in df.columns
        assert "f1_score" in df.columns
        assert "n_samples" in df.columns

    def test_calculate_metrics_with_misclassifications(self):
        """Test calculate_metrics with misclassifications."""
        monitor = ModelMonitor()

        # Add predictions with some errors
        monitor.add_prediction(np.array([0.6]), 1)  # Prediction: 1, Label: 1 (correct)
        monitor.add_prediction(np.array([0.7]), 0)  # Prediction: 1, Label: 0 (wrong)
        monitor.add_prediction(np.array([0.4]), 0)  # Prediction: 0, Label: 0 (correct)
        monitor.add_prediction(np.array([0.3]), 1)  # Prediction: 0, Label: 1 (wrong)

        metrics = monitor.calculate_metrics()

        assert "accuracy" in metrics
        # Accuracy should be 0.5 (2 correct out of 4)
        assert metrics["accuracy"] == 0.5


if __name__ == "__main__":
    pytest.main([__file__])
