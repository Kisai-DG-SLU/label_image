"""
Tests for logging utilities.
"""

import logging
import tempfile
from pathlib import Path

import pytest

from src.utils.logging import setup_logging


class TestSetupLogging:
    """Test setup_logging function."""

    def test_setup_logging_console_only(self):
        """Test logging setup with console output only."""
        logger = setup_logging(log_level="INFO", console=True)

        assert logger is not None
        assert logger.name == "brain-scan-ai"
        assert logger.level == logging.INFO

        # Should have at least one handler
        assert len(logger.handlers) >= 1

        # Check handler types
        handler_types = [type(h).__name__ for h in logger.handlers]
        assert "StreamHandler" in handler_types

    def test_setup_logging_file_only(self):
        """Test logging setup with file output only."""
        with tempfile.NamedTemporaryFile(suffix=".log", delete=False) as tmpfile:
            log_file = Path(tmpfile.name)

            logger = setup_logging(log_level="DEBUG", log_file=log_file, console=False)

            assert logger is not None
            assert logger.name == "brain-scan-ai"
            assert logger.level == logging.DEBUG

            # Should have file handler
            assert len(logger.handlers) == 1
            handler = logger.handlers[0]
            assert isinstance(handler, logging.FileHandler)

            # Check file was created
            assert log_file.exists()

            # Clean up
            log_file.unlink()

    def test_setup_logging_both_console_and_file(self):
        """Test logging setup with both console and file output."""
        with tempfile.NamedTemporaryFile(suffix=".log", delete=False) as tmpfile:
            log_file = Path(tmpfile.name)

            logger = setup_logging(log_level="WARNING", log_file=log_file, console=True)

            assert logger is not None
            assert logger.name == "brain-scan-ai"
            assert logger.level == logging.WARNING

            # Should have both handlers
            assert len(logger.handlers) >= 2

            # Check handler types
            handler_types = [type(h).__name__ for h in logger.handlers]
            assert "StreamHandler" in handler_types
            assert "FileHandler" in handler_types

            # Check file was created
            assert log_file.exists()

            # Clean up
            log_file.unlink()

    def test_setup_logging_different_levels(self):
        """Test logging setup with different log levels."""
        test_cases = [
            ("DEBUG", logging.DEBUG),
            ("INFO", logging.INFO),
            ("WARNING", logging.WARNING),
            ("ERROR", logging.ERROR),
            ("CRITICAL", logging.CRITICAL),
        ]

        for level_str, level_int in test_cases:
            logger = setup_logging(log_level=level_str, console=False)
            assert logger.level == level_int

    def test_setup_logging_creates_parent_directories(self):
        """Test that setup_logging creates parent directories for log file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            log_dir = Path(tmpdir) / "subdir" / "another"
            log_file = log_dir / "test.log"

            # Directory shouldn't exist yet
            assert not log_dir.exists()

            setup_logging(log_file=log_file, console=False)

            # Directory should be created
            assert log_dir.exists()
            assert log_file.exists()

            # Clean up
            log_file.unlink()

    def test_setup_logging_clears_existing_handlers(self):
        """Test that setup_logging clears existing handlers."""
        logger = logging.getLogger("brain-scan-ai")

        # Clear any existing handlers from previous tests
        logger.handlers.clear()

        # Add some dummy handlers
        dummy_handler1 = logging.NullHandler()
        dummy_handler2 = logging.NullHandler()
        logger.addHandler(dummy_handler1)
        logger.addHandler(dummy_handler2)

        assert len(logger.handlers) == 2

        # Call setup_logging
        logger = setup_logging(log_level="INFO", console=True)

        # Should have cleared old handlers and added new ones
        # With console=True and no log_file, we should have exactly 1 handler
        assert len(logger.handlers) == 1

        # None of the handlers should be the dummy ones
        handler_types = [type(h).__name__ for h in logger.handlers]
        assert "NullHandler" not in handler_types

    def test_logging_output(self):
        """Test that logging actually outputs messages."""
        import io
        import logging

        # Create a string stream to capture log output
        log_capture_string = io.StringIO()

        # Create a custom handler that writes to our string stream
        string_handler = logging.StreamHandler(log_capture_string)
        string_handler.setLevel(logging.INFO)
        # Use the same formatter as setup_logging
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        string_handler.setFormatter(formatter)

        # Get the logger and add our handler
        logger = setup_logging(
            log_level="INFO", console=False
        )  # Don't add console handler
        logger.addHandler(string_handler)

        # Log messages
        logger.info("Test message")
        logger.warning("Warning message")
        logger.error("Error message")

        # Get the log output
        output = log_capture_string.getvalue()

        # Check that messages appear in output
        assert "Test message" in output
        assert "Warning message" in output
        assert "Error message" in output
        assert "brain-scan-ai" in output


if __name__ == "__main__":
    pytest.main([__file__])
