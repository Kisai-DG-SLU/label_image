"""
Tests for the dashboard module.
"""

import sys
from unittest.mock import MagicMock, patch

import pytest


def test_dashboard_app():
    """Test that dashboard_app is correctly imported."""
    # Mock streamlit if not installed
    try:
        import streamlit as st
    except ImportError:
        st = MagicMock()
        sys.modules["streamlit"] = st

    from src.api.dashboard import dashboard_app

    # dashboard_app should be the streamlit module
    assert dashboard_app is not None
    # In the actual code, dashboard_app = st, so we're testing the import works


def test_main_function():
    """Test the main function with mocked streamlit."""

    # Mock streamlit functions
    mock_st = MagicMock()

    with patch.dict(sys.modules, {"streamlit": mock_st}):
        # Re-import to use the mocked streamlit
        import importlib

        import src.api.dashboard

        importlib.reload(src.api.dashboard)

        # Call main function
        src.api.dashboard.main()

        # Verify streamlit functions were called
        mock_st.title.assert_called_once_with("BrainScanAI Dashboard")
        mock_st.write.assert_called_once_with(
            "Dashboard for brain tumor detection visualization"
        )


def test_dashboard_imports():
    """Test that dashboard module imports correctly."""
    # Mock streamlit if not installed
    try:
        import streamlit as st
    except ImportError:
        st = MagicMock()
        sys.modules["streamlit"] = st

    from src.api.dashboard import dashboard_app, main

    assert dashboard_app is not None
    assert callable(main)


if __name__ == "__main__":
    pytest.main([__file__])
