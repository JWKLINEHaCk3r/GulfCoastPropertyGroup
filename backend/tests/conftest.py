"""Pytest configuration and shared fixtures."""
import pytest
import sys
from pathlib import Path

# Add backend app to path
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

@pytest.fixture
def mock_db_session():
    """Mock database session for testing."""
    from unittest.mock import MagicMock
    session = MagicMock()
    return session

@pytest.fixture
def mock_settings():
    """Mock application settings."""
    from unittest.mock import MagicMock
    settings = MagicMock()
    settings.database_url = "postgresql://test:test@localhost/test"
    settings.secret_key = "test-secret-key"
    settings.algorithm = "HS256"
    settings.access_token_expire_minutes = 30
    return settings

@pytest.fixture
def app():
    """Create FastAPI test app."""
    try:
        from app.main import app as fastapi_app
        return fastapi_app
    except Exception:
        return None

@pytest.fixture
def client(app):
    """FastAPI TestClient."""
    if app is None:
        return None
    from fastapi.testclient import TestClient
    return TestClient(app)

def pytest_configure(config):
    """Configure pytest markers."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
