import pytest
from api_report import create_app


@pytest.fixture
def app():
    return create_app(test_config=True)


@pytest.fixture
def client(app):
    return app.test_client()

