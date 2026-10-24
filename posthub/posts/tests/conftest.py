import pytest
from unittest.mock import Mock


@pytest.fixture
def sample_post():
    return {
        "id": 1,
        "title": "Test Post",
        "body": "A sample post used by automated tests.",
    }


@pytest.fixture
def mock_response(sample_post):
    response = Mock()
    response.status_code = 200
    response.json.return_value = sample_post
    return response
