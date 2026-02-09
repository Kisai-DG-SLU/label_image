"""
Data loading utilities for MRI datasets.

Simplified version following KISS principle.
"""

import warnings
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import torch
from torch.utils.data import DataLoader, Dataset

warnings.filterwarnings("ignore")


class MRIDataset(Dataset):
    """Dataset for MRI images."""

    def __init__(
        self, image_paths: list[Path], labels: list | None = None, transform=None
    ):
        self.image_paths = image_paths
        self.labels = labels
        self.transform = transform

    def __len__(self) -> int:
        return len(self.image_paths)

    def __getitem__(self, idx: int):
        # In real implementation, load actual MRI image
        # For now, return dummy data
        _ = self.image_paths[idx]  # Keep for future implementation

        # TODO: Implement actual image loading
        # For demo purposes, return random tensor
        image = torch.randn(3, 224, 224)

        if self.transform:
            image = self.transform(image)

        if self.labels is not None:
            label = self.labels[idx]
            return image, label

        return image


class DataLoaderWrapper:
    """Wrapper for data loading operations."""

    def __init__(self, data_dir: Path):
        self.data_dir = Path(data_dir)
        self.image_paths: list[Path] = []
        self.labels: list[int] = []

    def discover_images(self, extensions: list[str] | None = None):
        """Discover image files in data directory."""
        if extensions is None:
            extensions = [".png", ".jpg", ".jpeg", ".tiff"]

        self.image_paths = []
        for ext in extensions:
            self.image_paths.extend(list(self.data_dir.glob(f"**/*{ext}")))

        print(f"Found {len(self.image_paths)} images in {self.data_dir}")
        return self.image_paths

    def load_metadata(self, metadata_file: Path | None = None) -> pd.DataFrame:
        """Load metadata if available."""
        if metadata_file and metadata_file.exists():
            return pd.read_csv(metadata_file)
        return pd.DataFrame()

    def create_dataset(self, transform=None) -> MRIDataset:
        """Create MRI dataset from discovered images."""
        if not self.image_paths:
            self.discover_images()

        return MRIDataset(self.image_paths, self.labels, transform)

    def create_dataloader(
        self, batch_size: int = 32, shuffle: bool = True, transform=None
    ) -> DataLoader:
        """Create DataLoader for training/inference."""
        dataset = self.create_dataset(transform)
        return DataLoader(dataset, batch_size=batch_size, shuffle=shuffle)


def split_dataset(
    image_paths: list[Path],
    labels: list | None = None,
    train_ratio: float = 0.7,
    val_ratio: float = 0.15,
    random_seed: int = 42,
) -> dict[str, Any]:
    """
    Split dataset into train/val/test sets.

    Args:
        image_paths: List of image paths
        labels: Optional list of labels
        train_ratio: Ratio for training set
        val_ratio: Ratio for validation set
        random_seed: Random seed for reproducibility

    Returns:
        Dictionary with split indices
    """
    n_total = len(image_paths)
    indices = np.arange(n_total)
    np.random.seed(random_seed)
    np.random.shuffle(indices)

    n_train = int(n_total * train_ratio)
    n_val = int(n_total * val_ratio)
    n_test = n_total - n_train - n_val

    train_indices = indices[:n_train]
    val_indices = indices[n_train : n_train + n_val]
    test_indices = indices[n_train + n_val :]

    splits = {
        "train": {
            "indices": train_indices,
            "paths": [image_paths[i] for i in train_indices],
            "labels": [labels[i] for i in train_indices] if labels else None,
        },
        "val": {
            "indices": val_indices,
            "paths": [image_paths[i] for i in val_indices],
            "labels": [labels[i] for i in val_indices] if labels else None,
        },
        "test": {
            "indices": test_indices,
            "paths": [image_paths[i] for i in test_indices],
            "labels": [labels[i] for i in test_indices] if labels else None,
        },
    }

    print(f"Dataset split: Train={n_train}, Val={n_val}, Test={n_test}")
    return splits
