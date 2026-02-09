"""
Model monitoring module for BrainScanAI.

Provides monitoring and evaluation utilities for model performance tracking.
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.metrics import auc, classification_report, confusion_matrix, roc_curve


class ModelMonitor:
    """Monitor model performance and track metrics."""

    def __init__(self, model_name: str = "brain-scan-ai"):
        self.model_name = model_name
        self.metrics_history: list[dict[str, float]] = []
        self.predictions: list[np.ndarray] = []
        self.labels: list[int] = []

    def add_prediction(self, prediction: np.ndarray, label: int):
        """Add a prediction-label pair for evaluation."""
        self.predictions.append(prediction)
        self.labels.append(label)

    def calculate_metrics(self) -> dict[str, float]:
        """Calculate performance metrics from accumulated predictions."""
        if len(self.predictions) == 0:
            return {}

        predictions_array = np.array(self.predictions)
        labels_array = np.array(self.labels)

        # For binary classification
        if predictions_array.ndim > 1 and predictions_array.shape[1] == 2:
            pred_classes = np.argmax(predictions_array, axis=1)
        else:
            pred_classes = (predictions_array > 0.5).astype(int)

        # Calculate metrics
        report = classification_report(labels_array, pred_classes, output_dict=True)

        metrics = {
            "accuracy": report["accuracy"],
            "precision": report["weighted avg"]["precision"],
            "recall": report["weighted avg"]["recall"],
            "f1_score": report["weighted avg"]["f1-score"],
            "n_samples": len(self.predictions),
        }

        # Store in history
        self.metrics_history.append(metrics.copy())
        return metrics

    def plot_confusion_matrix(self, save_path: str | None = None):
        """Plot confusion matrix."""
        if len(self.predictions) == 0:
            return

        predictions_array = np.array(self.predictions)
        labels_array = np.array(self.labels)

        if predictions_array.ndim > 1 and predictions_array.shape[1] == 2:
            pred_classes = np.argmax(predictions_array, axis=1)
        else:
            pred_classes = (predictions_array > 0.5).astype(int)

        cm = confusion_matrix(labels_array, pred_classes)

        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
        plt.title(f"Confusion Matrix - {self.model_name}")
        plt.ylabel("True Label")
        plt.xlabel("Predicted Label")

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches="tight")
        plt.show()

    def plot_roc_curve(self, save_path: str | None = None):
        """Plot ROC curve."""
        if len(self.predictions) == 0:
            return

        predictions_array = np.array(self.predictions)
        labels_array = np.array(self.labels)

        # For binary classification with probability scores
        if predictions_array.ndim > 1 and predictions_array.shape[1] == 2:
            scores = predictions_array[:, 1]
        else:
            scores = predictions_array.flatten()

        fpr, tpr, _ = roc_curve(labels_array, scores)
        roc_auc = auc(fpr, tpr)

        plt.figure(figsize=(8, 6))
        plt.plot(
            fpr, tpr, color="darkorange", lw=2, label=f"ROC curve (AUC = {roc_auc:.2f})"
        )
        plt.plot([0, 1], [0, 1], color="navy", lw=2, linestyle="--")
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel("False Positive Rate")
        plt.ylabel("True Positive Rate")
        plt.title(f"ROC Curve - {self.model_name}")
        plt.legend(loc="lower right")

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches="tight")
        plt.show()

    def get_history_df(self) -> pd.DataFrame:
        """Get metrics history as DataFrame."""
        return pd.DataFrame(self.metrics_history)
