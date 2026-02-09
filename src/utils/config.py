"""
Configuration module for BrainScanAI.

Centralized configuration management using Hydra.
"""

from dataclasses import dataclass


@dataclass
class Config:
    """Main configuration class."""

    # Data paths
    data_dir: str = "data"
    raw_dir: str = "data/raw"
    processed_dir: str = "data/processed"

    # Model parameters
    model_name: str = "resnet50"
    image_size: tuple = (224, 224)
    batch_size: int = 32
    num_epochs: int = 50
    learning_rate: float = 0.001

    # Clustering parameters
    n_clusters: int = 5
    clustering_algorithm: str = "kmeans"

    # Training parameters
    validation_split: float = 0.15
    test_split: float = 0.15
    random_seed: int = 42

    # Logging
    log_dir: str = "logs"
    experiment_name: str = "brain-scan-ai"

    @classmethod
    def from_dict(cls, config_dict: dict) -> "Config":
        """Create Config instance from dictionary."""
        return cls(**config_dict)
