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

        # Determine prediction classes
        if predictions_array.ndim == 1:
            # Single probability per sample (binary classification)
            pred_classes = (predictions_array > 0.5).astype(int)
        elif predictions_array.shape[1] == 1:
            # Single probability per sample but 2D array
            pred_classes = (predictions_array.flatten() > 0.5).astype(int)
        else:
            # Multiple probabilities per sample (multiclass classification)
            pred_classes = np.argmax(predictions_array, axis=1)

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

        # Determine prediction classes (same logic as calculate_metrics)
        if predictions_array.ndim == 1:
            # Single probability per sample (binary classification)
            pred_classes = (predictions_array > 0.5).astype(int)
        elif predictions_array.shape[1] == 1:
            # Single probability per sample but 2D array
            pred_classes = (predictions_array.flatten() > 0.5).astype(int)
        else:
            # Multiple probabilities per sample (multiclass classification)
            pred_classes = np.argmax(predictions_array, axis=1)

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

        # ROC curve is only defined for binary classification
        # Determine if we have binary classification (2 classes)
        unique_labels = np.unique(labels_array)
        if len(unique_labels) > 2:
            # Multiclass classification - ROC curve not defined
            print(
                "Warning: ROC curve is only defined for binary classification. Skipping plot."
            )
            return

        # Extract scores for binary classification
        if predictions_array.ndim == 1:
            # Single probability per sample (binary classification)
            scores = predictions_array
        elif predictions_array.shape[1] == 1:
            # Single probability per sample but 2D array
            scores = predictions_array.flatten()
        elif predictions_array.shape[1] == 2:
            # Two probabilities per sample (binary with probability for each class)
            scores = predictions_array[:, 1]  # Use probability of positive class
        else:
            # Multiclass probabilities - use probability of positive class (class 1)
            # This assumes binary classification with one-hot encoded predictions
            if 1 in unique_labels:
                scores = predictions_array[:, 1]
            else:
                scores = predictions_array[:, -1]

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
