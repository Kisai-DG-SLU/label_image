"""
Pytest configuration for BrainScanAI tests.
"""
import matplotlib
import pytest

# Use non-interactive backend for matplotlib to prevent opening windows
matplotlib.use("Agg")


@pytest.fixture(autouse=True)
def mock_plt_show():
    """Mock plt.show() to prevent opening windows during tests."""
    import matplotlib.pyplot as plt
    with pytest.MonkeyPatch().context() as mp:
        mp.setattr(plt, "show", lambda: None)
        yield