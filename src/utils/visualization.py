"""
Visualization utilities for BrainScanAI.

Provides plotting and visualization functions for model results.
"""

from typing import Any

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


def plot_results(
    metrics: dict[str, Any],
    save_path: str | None = None,
    title: str = "Model Results",
) -> None:
    """
    Plot model evaluation results.

    Args:
        metrics: Dictionary containing evaluation metrics
        save_path: Optional path to save the plot
        title: Plot title
    """
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # Plot metrics bar chart
    if "accuracy" in metrics:
        metric_names = ["accuracy", "precision", "recall", "f1_score"]
        metric_values = [metrics.get(m, 0) for m in metric_names]

        axes[0].bar(metric_names, metric_values)
        axes[0].set_title("Classification Metrics")
        axes[0].set_ylim([0, 1])
        axes[0].set_ylabel("Score")

        # Add value labels on bars
        for i, v in enumerate(metric_values):
            axes[0].text(i, v + 0.02, f"{v:.3f}", ha="center")

    # Plot confusion matrix if available
    if "confusion_matrix" in metrics:
        cm = metrics["confusion_matrix"]
        sns.heatmap(cm, annot=True, fmt="d", ax=axes[1])
        axes[1].set_title("Confusion Matrix")
        axes[1].set_xlabel("Predicted")
        axes[1].set_ylabel("True")

    plt.suptitle(title)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.show()


def plot_clustering_results(
    features: np.ndarray,
    labels: np.ndarray,
    reduced_features: np.ndarray | None = None,
    save_path: str | None = None,
) -> None:
    """
    Plot clustering results.

    Args:
        features: Original feature vectors
        labels: Cluster labels
        reduced_features: Reduced dimensionality features (2D or 3D)
        save_path: Optional path to save the plot
    """
    if reduced_features is None:
        # Use first 2 principal components if not provided
        from sklearn.decomposition import PCA

        pca = PCA(n_components=2)
        reduced_features = pca.fit_transform(features)

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # Scatter plot of clusters
    scatter = axes[0].scatter(
        reduced_features[:, 0],
        reduced_features[:, 1],
        c=labels,
        cmap="tab10",
        alpha=0.6,
    )
    axes[0].set_title("Cluster Visualization")
    axes[0].set_xlabel("Component 1")
    axes[0].set_ylabel("Component 2")
    plt.colorbar(scatter, ax=axes[0])

    # Histogram of cluster sizes
    unique_labels, counts = np.unique(labels, return_counts=True)
    axes[1].bar(unique_labels, counts)
    axes[1].set_title("Cluster Sizes")
    axes[1].set_xlabel("Cluster Label")
    axes[1].set_ylabel("Number of Samples")

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.show()


def plot_training_history(
    history: dict[str, list[float]], save_path: str | None = None
) -> None:
    """
    Plot training history (loss and accuracy over epochs).

    Args:
        history: Dictionary with keys like 'loss', 'val_loss', 'accuracy', 'val_accuracy'
        save_path: Optional path to save the plot
    """
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # Plot loss
    if "loss" in history:
        axes[0].plot(history["loss"], label="Training Loss")
    if "val_loss" in history:
        axes[0].plot(history["val_loss"], label="Validation Loss")
    axes[0].set_title("Loss over Epochs")
    axes[0].set_xlabel("Epoch")
    axes[0].set_ylabel("Loss")
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    # Plot accuracy
    if "accuracy" in history:
        axes[1].plot(history["accuracy"], label="Training Accuracy")
    if "val_accuracy" in history:
        axes[1].plot(history["val_accuracy"], label="Validation Accuracy")
    axes[1].set_title("Accuracy over Epochs")
    axes[1].set_xlabel("Epoch")
    axes[1].set_ylabel("Accuracy")
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.show()
