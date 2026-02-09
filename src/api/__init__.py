"""
API module for BrainScanAI

Contains FastAPI application and Streamlit dashboard for the brain tumor detection system.
"""

from .main import app

# Temporarily comment out dashboard import for CI/CD testing
# from .dashboard import dashboard_app

__all__ = ["app"]  # , "dashboard_app"]
