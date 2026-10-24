import requests
import pytest
from unittest.mock import Mock

from posts import services
from posts.services import ExternalAPIError, PostNotFoundError


def test_fetch_post_success(mocker, sample_post, mock_response):
    get = mocker.patch("posts.services.requests.get", return_value=mock_response)

    result = services.fetch_post(1)

    assert result == sample_post
    get.assert_called_once_with(
        "https://jsonplaceholder.typicode.com/posts/1", timeout=5
    )


def test_fetch_posts_success(mocker, sample_post):
    response = Mock(status_code=200)
    response.json.return_value = [sample_post, {**sample_post, "id": 2}]
    mocker.patch("posts.services.requests.get", return_value=response)

    result = services.fetch_posts()

    assert len(result) == 2
    assert result[1]["id"] == 2


def test_fetch_post_404_raises_not_found(mocker):
    response = Mock(status_code=404)
    mocker.patch("posts.services.requests.get", return_value=response)

    with pytest.raises(PostNotFoundError, match="Post not found"):
        services.fetch_post(999)


def test_fetch_post_server_error(mocker):
    response = Mock(status_code=503)
    mocker.patch("posts.services.requests.get", return_value=response)

    with pytest.raises(ExternalAPIError, match="server error"):
        services.fetch_post(1)


def test_fetch_post_timeout(mocker):
    mocker.patch(
        "posts.services.requests.get",
        side_effect=requests.Timeout("request timed out"),
    )

    with pytest.raises(ExternalAPIError, match="timed out"):
        services.fetch_post(1)


def test_fetch_post_connection_error(mocker):
    mocker.patch(
        "posts.services.requests.get",
        side_effect=requests.ConnectionError("offline"),
    )

    with pytest.raises(ExternalAPIError, match="connect"):
        services.fetch_post(1)


def test_fetch_post_invalid_json(mocker):
    response = Mock(status_code=200)
    response.json.side_effect = ValueError("invalid JSON")
    mocker.patch("posts.services.requests.get", return_value=response)

    with pytest.raises(ExternalAPIError, match="invalid JSON"):
        services.fetch_post(1)


def test_fetch_post_unexpected_shape(mocker):
    response = Mock(status_code=200)
    response.json.return_value = {"id": 1, "title": "Missing body"}
    mocker.patch("posts.services.requests.get", return_value=response)

    with pytest.raises(ExternalAPIError, match="unexpected response"):
        services.fetch_post(1)


def test_fetch_posts_unexpected_shape(mocker):
    response = Mock(status_code=200)
    response.json.return_value = {"not": "a list"}
    mocker.patch("posts.services.requests.get", return_value=response)

    with pytest.raises(ExternalAPIError, match="unexpected response"):
        services.fetch_posts()

def test_fetch_post_client_error(mocker):
    response = Mock(status_code=400)
    mocker.patch("posts.services.requests.get", return_value=response)

    with pytest.raises(ExternalAPIError, match="rejected the request"):
        services.fetch_post(1)


def test_fetch_posts_invalid_item(mocker, sample_post):
    response = Mock(status_code=200)
    response.json.return_value = [
        sample_post,
        {"id": 2, "title": "Missing body"},
    ]
    mocker.patch("posts.services.requests.get", return_value=response)

    with pytest.raises(ExternalAPIError, match="unexpected response"):
        services.fetch_posts()