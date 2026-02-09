"""
Basic tests for BrainScanAI project.

Following KISS principle and credit-scoring-app patterns.
"""

from pathlib import Path

import pytest
import torch

# Test data paths
DATA_DIR = Path(__file__).parent.parent / "data"


def test_data_directory_exists():
    """Test that data directory exists and has expected structure."""
    assert DATA_DIR.exists(), "Data directory should exist"
    assert (DATA_DIR / "avec_labels").exists(), "Labeled data directory should exist"
    assert (DATA_DIR / "sans_label").exists(), "Unlabeled data directory should exist"

    # Check for dataset description file
    txt_files = list(DATA_DIR.glob("*.txt"))
    assert len(txt_files) > 0, "Should have dataset description file"


def test_imports():
    """Test that main modules can be imported."""
    try:
        from src.data.loader import DataLoaderWrapper, MRIDataset
        from src.model.features import FeatureExtractor
        from src.model.preprocessing import ImagePreprocessor

        # Test instantiation of imported classes
        dataset = MRIDataset(image_paths=[], labels=None)
        assert dataset is not None

        preprocessor = ImagePreprocessor(image_size=(224, 224))
        assert preprocessor.image_size == (224, 224)

        # FeatureExtractor requires torch, skip instantiation if torch not available
        # Just verify import succeeded
        assert FeatureExtractor is not None

        # DataLoaderWrapper requires a Path
        import tempfile
        from pathlib import Path

        with tempfile.TemporaryDirectory() as tmpdir:
            wrapper = DataLoaderWrapper(data_dir=Path(tmpdir))
            assert wrapper is not None

    except ImportError as e:
        pytest.fail(f"Import failed: {e}")


def test_preprocessing():
    """Test image preprocessing functionality."""
    from src.model.preprocessing import ImagePreprocessor

    preprocessor = ImagePreprocessor(image_size=(224, 224))
    assert preprocessor.image_size == (224, 224)
    assert preprocessor.transform is not None

    # Test transform creation
    transform = preprocessor._create_transform()
    assert transform is not None


def test_feature_extractor():
    """Test feature extractor initialization."""
    from src.model.features import FeatureExtractor

    # Test CPU mode
    extractor = FeatureExtractor(model_name="resnet50", device="cpu")
    assert extractor.device.type == "cpu"
    assert extractor.model_name == "resnet50"
    assert extractor.feature_dim == 2048

    # Test model loading
    assert extractor.model is not None

    # Test feature dimension
    assert extractor._get_feature_dimension() == 2048


def test_data_loader():
    """Test data loader functionality."""
    from src.data.loader import DataLoaderWrapper, split_dataset

    # Test wrapper initialization
    wrapper = DataLoaderWrapper(DATA_DIR)
    assert wrapper.data_dir == DATA_DIR

    # Test dataset splitting
    dummy_paths = [Path(f"image_{i}.png") for i in range(100)]
    dummy_labels = [i % 2 for i in range(100)]  # Binary labels

    splits = split_dataset(dummy_paths, dummy_labels)
    assert "train" in splits
    assert "val" in splits
    assert "test" in splits

    # Check split sizes
    assert len(splits["train"]["paths"]) == 70  # 70% of 100
    assert len(splits["val"]["paths"]) == 15  # 15% of 100
    assert len(splits["test"]["paths"]) == 15  # 15% of 100


def test_torch_available():
    """Test that PyTorch is available."""
    assert torch.__version__ is not None
    print(f"PyTorch version: {torch.__version__}")

    # Test CUDA availability (optional)
    cuda_available = torch.cuda.is_available()
    print(f"CUDA available: {cuda_available}")


if __name__ == "__main__":
    # Run tests manually
    test_data_directory_exists()
    test_imports()
    test_preprocessing()
    test_feature_extractor()
    test_data_loader()
    test_torch_available()
    print("All basic tests passed!")
