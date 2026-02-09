"""
Data augmentation module for BrainScanAI.

Provides data augmentation utilities for MRI images.
"""

import torch
import torchvision.transforms as transforms


class DataAugmentor:
    """Data augmentation for MRI images."""

    def __init__(self, augmentations: list[str] | None = None):
        self.augmentations = augmentations or [
            "random_flip",
            "random_rotation",
            "random_brightness",
            "random_contrast",
        ]

    def get_transform(self, train: bool = True) -> transforms.Compose:
        """Get transformation pipeline."""
        base_transforms = [
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ]

        if train:
            augment_transforms = []
            if "random_flip" in self.augmentations:
                augment_transforms.append(transforms.RandomHorizontalFlip(p=0.5))
                augment_transforms.append(transforms.RandomVerticalFlip(p=0.5))

            if "random_rotation" in self.augmentations:
                augment_transforms.append(transforms.RandomRotation(degrees=15))

            if "random_brightness" in self.augmentations:
                augment_transforms.append(transforms.ColorJitter(brightness=0.2))

            if "random_contrast" in self.augmentations:
                augment_transforms.append(transforms.ColorJitter(contrast=0.2))

            # Combine augmentations with base transforms
            all_transforms = augment_transforms + base_transforms
        else:
            all_transforms = base_transforms

        return transforms.Compose(all_transforms)

    def augment_batch(self, images: torch.Tensor) -> torch.Tensor:
        """Apply augmentations to a batch of images."""
        transform = self.get_transform(train=True)
        augmented = []
        for img in images:
            # Convert tensor to PIL for augmentation
            img_pil = transforms.ToPILImage()(img)
            augmented_img = transform(img_pil)
            augmented.append(augmented_img)
        return torch.stack(augmented)
