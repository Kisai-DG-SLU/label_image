"""
Dataset module for BrainScanAI.

Contains dataset classes for MRI image loading and management.
"""

from pathlib import Path

import torch
from torch.utils.data import Dataset


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

    def __getitem__(self, idx: int) -> tuple[torch.Tensor, int | None]:
        """Get image and label at index."""
        # This is a placeholder - actual implementation would load images
        # For now, return dummy data
        image = torch.randn(3, 224, 224)  # Random tensor as placeholder
        label = self.labels[idx] if self.labels is not None else -1

        if self.transform:
            image = self.transform(image)

        return image, label
