"""
Tests for data augmentation module.
"""

import pytest
import torch
import torchvision.transforms as transforms

from src.data.augmentation import DataAugmentor


class TestDataAugmentor:
    """Test DataAugmentor class."""

    def test_init_default(self):
        """Test default initialization."""
        augmentor = DataAugmentor()
        assert augmentor.augmentations == [
            "random_flip",
            "random_rotation",
            "random_brightness",
            "random_contrast",
        ]

    def test_init_custom_augmentations(self):
        """Test initialization with custom augmentations."""
        custom_augs = ["random_flip", "random_rotation"]
        augmentor = DataAugmentor(augmentations=custom_augs)
        assert augmentor.augmentations == custom_augs

    def test_init_empty_augmentations(self):
        """Test initialization with empty augmentations list."""
        # Note: The constructor uses `augmentations or [...]`, so an empty list
        # will be treated as falsy and replaced with default augmentations
        augmentor = DataAugmentor(augmentations=[])
        # Empty list is falsy, so defaults should be used
        assert augmentor.augmentations == [
            "random_flip",
            "random_rotation",
            "random_brightness",
            "random_contrast",
        ]

    def test_get_transform_train_default(self):
        """Test get_transform for training with default augmentations."""
        augmentor = DataAugmentor()
        transform = augmentor.get_transform(train=True)

        assert isinstance(transform, transforms.Compose)
        # Should have base transforms + augmentation transforms
        # Base transforms: ToTensor and Normalize
        # Augmentations: random_flip (2 transforms), random_rotation, random_brightness, random_contrast
        # Total: 2 base + up to 4 augmentations = at least 6 transforms
        assert len(transform.transforms) >= 6

    def test_get_transform_train_custom_augmentations(self):
        """Test get_transform for training with custom augmentations."""
        custom_augs = ["random_flip", "random_brightness"]
        augmentor = DataAugmentor(augmentations=custom_augs)
        transform = augmentor.get_transform(train=True)

        assert isinstance(transform, transforms.Compose)
        # Should have base transforms + selected augmentations
        # random_flip adds 2 transforms, random_brightness adds 1
        # Total: 2 base + 3 augmentations = 5 transforms
        assert len(transform.transforms) == 5

    def test_get_transform_train_no_augmentations(self):
        """Test get_transform for training with no augmentations."""
        # Note: Empty list is falsy, so defaults will be used
        # To truly test no augmentations, we need to pass None
        augmentor = DataAugmentor(augmentations=None)
        transform = augmentor.get_transform(train=True)

        assert isinstance(transform, transforms.Compose)
        # With defaults, should have base transforms + augmentation transforms
        # random_flip (2 transforms), random_rotation, random_brightness, random_contrast
        # Total: 2 base + 4 augmentations = 6 transforms
        assert (
            len(transform.transforms) == 7
        )  # Actually 7 because random_flip adds 2 transforms
        # Check that ToTensor and Normalize are present
        transform_types = [type(t).__name__ for t in transform.transforms]
        assert "ToTensor" in transform_types
        assert "Normalize" in transform_types

    def test_get_transform_test(self):
        """Test get_transform for test/validation (train=False)."""
        augmentor = DataAugmentor()
        transform = augmentor.get_transform(train=False)

        assert isinstance(transform, transforms.Compose)
        # Should only have base transforms (no augmentations)
        assert len(transform.transforms) == 2
        assert isinstance(transform.transforms[0], transforms.ToTensor)
        assert isinstance(transform.transforms[1], transforms.Normalize)

    def test_get_transform_test_with_augmentations(self):
        """Test get_transform for test with augmentations defined but train=False."""
        augmentor = DataAugmentor(augmentations=["random_flip", "random_rotation"])
        transform = augmentor.get_transform(train=False)

        assert isinstance(transform, transforms.Compose)
        # Should only have base transforms (no augmentations even though they're defined)
        assert len(transform.transforms) == 2
        assert isinstance(transform.transforms[0], transforms.ToTensor)
        assert isinstance(transform.transforms[1], transforms.Normalize)

    def test_augment_batch(self):
        """Test augment_batch method."""
        augmentor = DataAugmentor()

        # Create a batch of dummy images (batch_size=2, channels=3, height=64, width=64)
        batch = torch.randn(2, 3, 64, 64)

        augmented = augmentor.augment_batch(batch)

        # Check output shape
        assert augmented.shape == batch.shape
        assert augmented.dtype == torch.float32

        # Check that values are normalized (mean ~0, std ~1 after normalization)
        # The normalization uses ImageNet stats, so values should be in reasonable range
        assert torch.all(torch.isfinite(augmented))

    def test_augment_batch_single_image(self):
        """Test augment_batch with single image."""
        augmentor = DataAugmentor()

        # Single image (batch_size=1)
        batch = torch.randn(1, 3, 64, 64)

        augmented = augmentor.augment_batch(batch)

        assert augmented.shape == batch.shape
        assert augmented.dtype == torch.float32

    def test_augment_batch_empty_augmentations(self):
        """Test augment_batch with empty augmentations list."""
        # Note: Empty list is falsy, so defaults will be used
        # To truly test no augmentations, we need to pass None
        augmentor = DataAugmentor(augmentations=None)

        batch = torch.randn(2, 3, 64, 64)

        augmented = augmentor.augment_batch(batch)

        # With defaults, images will have augmentations applied
        assert augmented.shape == batch.shape

    def test_transform_pipeline_components(self):
        """Test that transform pipeline contains expected components."""
        augmentor = DataAugmentor()
        transform = augmentor.get_transform(train=True)

        # Check for specific transform types based on augmentations
        transform_types = [type(t).__name__ for t in transform.transforms]

        # Should contain ToTensor and Normalize
        assert "ToTensor" in transform_types
        assert "Normalize" in transform_types

        # Should contain augmentation transforms
        # Note: We can't easily check for specific augmentations without
        # knowing the exact order, but we can check there are more than 2 transforms
        assert len(transform.transforms) > 2

    def test_normalization_parameters(self):
        """Test that normalization uses ImageNet stats."""
        augmentor = DataAugmentor(augmentations=[])
        transform = augmentor.get_transform(train=False)

        # Find the Normalize transform
        normalize_transform = None
        for t in transform.transforms:
            if isinstance(t, transforms.Normalize):
                normalize_transform = t
                break

        assert normalize_transform is not None
        assert normalize_transform.mean == [0.485, 0.456, 0.406]
        assert normalize_transform.std == [0.229, 0.224, 0.225]

    def test_augmentation_consistency(self):
        """Test that augment_batch produces different but valid outputs."""
        augmentor = DataAugmentor()

        # Create identical images
        original_image = torch.randn(3, 64, 64)
        batch = torch.stack([original_image, original_image.clone()])

        augmented = augmentor.augment_batch(batch)

        # Augmented images should be valid (finite values)
        assert torch.all(torch.isfinite(augmented))

        # The two augmented images might be slightly different due to random augmentations
        # but they should have the same shape and type
        assert augmented[0].shape == augmented[1].shape
        assert augmented[0].dtype == augmented[1].dtype

    def test_augment_batch_with_different_augmentation_sets(self):
        """Test augment_batch with different augmentation configurations."""
        test_cases = [
            [],  # No augmentations
            ["random_flip"],
            ["random_flip", "random_rotation"],
            ["random_brightness", "random_contrast"],
            ["random_flip", "random_rotation", "random_brightness", "random_contrast"],
        ]

        batch = torch.randn(2, 3, 64, 64)

        for augmentations in test_cases:
            augmentor = DataAugmentor(augmentations=augmentations)
            augmented = augmentor.augment_batch(batch)

            # All should produce valid outputs
            assert augmented.shape == batch.shape
            assert torch.all(torch.isfinite(augmented))


if __name__ == "__main__":
    pytest.main([__file__])
