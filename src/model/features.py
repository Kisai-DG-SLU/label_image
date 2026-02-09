"""
Feature extraction module for MRI images using pre-trained models.

Adapted from credit-scoring-app patterns for computer vision.
"""

from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
import torchvision.models as models


class FeatureExtractor:
    """Extract features from MRI images using pre-trained models."""

    def __init__(self, model_name: str = "resnet50", device: str = "cuda"):
        self.device = torch.device(device if torch.cuda.is_available() else "cpu")
        self.model_name = model_name
        self.model = self._load_pretrained_model()
        self.feature_dim = self._get_feature_dimension()

    def _load_pretrained_model(self) -> nn.Module:
        """Load pre-trained model and remove classification layer."""
        if self.model_name == "resnet50":
            model = models.resnet50(weights=models.ResNet50_Weights.IMAGENET1K_V1)
            # Remove the final fully connected layer
            model = nn.Sequential(*list(model.children())[:-1])
        elif self.model_name == "resnet18":
            model = models.resnet18(weights=models.ResNet18_Weights.IMAGENET1K_V1)
            model = nn.Sequential(*list(model.children())[:-1])
        elif self.model_name == "vgg16":
            model = models.vgg16(weights=models.VGG16_Weights.IMAGENET1K_V1)
            model.classifier = nn.Sequential(*list(model.classifier.children())[:-1])
        else:
            raise ValueError(f"Unsupported model: {self.model_name}")

        model = model.to(self.device)
        model.eval()
        return model

    def _get_feature_dimension(self) -> int:
        """Get the dimension of extracted features."""
        if self.model_name.startswith("resnet"):
            return 2048 if "50" in self.model_name else 512
        elif self.model_name == "vgg16":
            return 4096
        else:
            return 512

    def extract_features(self, images: torch.Tensor) -> np.ndarray:
        """
        Extract features from batch of images.

        Args:
            images: Tensor of shape (batch_size, channels, height, width)

        Returns:
            features: Array of shape (batch_size, feature_dim)
        """
        with torch.no_grad():
            images = images.to(self.device)
            features = self.model(images)
            features = features.view(features.size(0), -1)
            return features.cpu().numpy()

    def extract_features_from_paths(
        self, image_paths: list[Path], preprocessor, batch_size: int = 32
    ) -> np.ndarray:
        """
        Extract features from list of image paths.

        Args:
            image_paths: List of Path objects to images
            preprocessor: ImagePreprocessor instance
            batch_size: Batch size for processing

        Returns:
            features: Array of shape (n_images, feature_dim)
        """
        all_features = []

        for i in range(0, len(image_paths), batch_size):
            batch_paths = image_paths[i : i + batch_size]
            batch_images = preprocessor.load_images(batch_paths)
            batch_features = self.extract_features(batch_images)
            all_features.append(batch_features)

        return np.vstack(all_features)


def create_feature_extractor(model_name: str = "resnet50", device: str = "cuda"):
    """Factory function to create feature extractor."""
    return FeatureExtractor(model_name=model_name, device=device)
