import requests
from unittest.mock import Mock


def test_detail_endpoint_success(client, mocker, sample_post):
    response = Mock(status_code=200)
    response.json.return_value = sample_post
    get = mocker.patch("posts.services.requests.get", return_value=response)

    api_response = client.get("/api/posts/1/")

    assert api_response.status_code == 200
    assert api_response.json() == sample_post
    get.assert_called_once()


def test_list_endpoint_success(client, mocker, sample_post):
    response = Mock(status_code=200)
    response.json.return_value = [sample_post]
    mocker.patch("posts.services.requests.get", return_value=response)

    api_response = client.get("/api/posts/")

    assert api_response.status_code == 200
    assert api_response.json() == {"results": [sample_post], "count": 1}


def test_detail_endpoint_not_found(client, mocker):
    response = Mock(status_code=404)
    mocker.patch("posts.services.requests.get", return_value=response)

    api_response = client.get("/api/posts/999/")

    assert api_response.status_code == 404
    assert api_response.json() == {"error": "Post not found."}


def test_detail_endpoint_upstream_timeout(client, mocker):
    mocker.patch(
        "posts.services.requests.get",
        side_effect=requests.Timeout("slow"),
    )

    api_response = client.get("/api/posts/1/")

    assert api_response.status_code == 502
    assert "timed out" in api_response.json()["error"]


def test_detail_endpoint_invalid_id(client):
    api_response = client.get("/api/posts/0/")

    assert api_response.status_code == 400
    assert api_response.json() == {
        "error": "post_id must be a positive integer."
    }


def test_endpoint_rejects_post_method(client):
    api_response = client.post("/api/posts/1/")

    assert api_response.status_code == 405

def test_list_endpoint_upstream_error(client, mocker):
    mocker.patch(
        "posts.services.requests.get",
        side_effect=requests.Timeout("request timed out"),
    )

    response = client.get("/api/posts/")

    assert response.status_code == 502
    assert response.json() == {
        "error": "The external API request timed out."
    }