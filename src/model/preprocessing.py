"""
Preprocessing module for MRI images.

Adapted from credit-scoring-app patterns but specialized for computer vision.
"""

from pathlib import Path

import torch
import torchvision.transforms as transforms
from PIL import Image


class ImagePreprocessor:
    """Preprocess MRI images for model input."""

    def __init__(self, image_size: tuple[int, int] = (224, 224)):
        self.image_size = image_size
        self.transform = self._create_transform()

    def _create_transform(self):
        """Create transformation pipeline for MRI images."""
        return transforms.Compose(
            [
                transforms.Resize(self.image_size),
                transforms.ToTensor(),
                transforms.Normalize(
                    mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]
                ),
            ]
        )

    def load_image(self, image_path: Path) -> torch.Tensor:
        """Load and preprocess a single image."""
        try:
            image = Image.open(image_path).convert("RGB")
            return self.transform(image)
        except Exception as e:
            raise ValueError(f"Error loading image {image_path}: {e}") from e

    def load_images(self, image_paths: list[Path]) -> torch.Tensor:
        """Load and preprocess multiple images."""
        images = []
        for path in image_paths:
            images.append(self.load_image(path))
        return torch.stack(images)

    def augment_image(self, image: torch.Tensor) -> torch.Tensor:
        """Apply data augmentation to image."""
        aug_transform = transforms.Compose(
            [
                transforms.RandomHorizontalFlip(p=0.5),
                transforms.RandomRotation(degrees=15),
                transforms.ColorJitter(brightness=0.2, contrast=0.2),
            ]
        )
        return aug_transform(image)


def create_dataset_transform(train: bool = True) -> transforms.Compose:
    """Create transform for dataset based on train/val/test mode."""
    if train:
        return transforms.Compose(
            [
                transforms.Resize((224, 224)),
                transforms.RandomHorizontalFlip(),
                transforms.RandomRotation(15),
                transforms.ToTensor(),
                transforms.Normalize(
                    mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]
                ),
            ]
        )
    else:
        return transforms.Compose(
            [
                transforms.Resize((224, 224)),
                transforms.ToTensor(),
                transforms.Normalize(
                    mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]
                ),
            ]
        )
