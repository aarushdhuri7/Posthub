"""Service layer for communicating with JSONPlaceholder."""

import requests

BASE_URL = "https://jsonplaceholder.typicode.com"
TIMEOUT_SECONDS = 5


class ExternalAPIError(Exception):
    """Raised when the external API cannot provide a usable response."""


class PostNotFoundError(ExternalAPIError):
    """Raised when JSONPlaceholder reports that a post does not exist."""


def _get_json(url):
    """Fetch JSON and normalize common network/response errors."""
    try:
        response = requests.get(url, timeout=TIMEOUT_SECONDS)
    except requests.Timeout as exc:
        raise ExternalAPIError("The external API request timed out.") from exc
    except requests.RequestException as exc:
        raise ExternalAPIError("Could not connect to the external API.") from exc

    if response.status_code == 404:
        raise PostNotFoundError("Post not found.")
    if response.status_code >= 500:
        raise ExternalAPIError("The external API returned a server error.")
    if response.status_code >= 400:
        raise ExternalAPIError("The external API rejected the request.")

    try:
        return response.json()
    except (ValueError, requests.exceptions.JSONDecodeError) as exc:
        raise ExternalAPIError("The external API returned invalid JSON.") from exc


def fetch_post(post_id):
    """Fetch one post, validating the response shape."""
    data = _get_json(f"{BASE_URL}/posts/{post_id}")
    if not isinstance(data, dict) or not {"id", "title", "body"}.issubset(data):
        raise ExternalAPIError("The external API returned an unexpected response.")
    return {"id": data["id"], "title": data["title"], "body": data["body"]}


def fetch_posts():
    """Fetch the post collection, validating the response shape."""
    data = _get_json(f"{BASE_URL}/posts")
    if not isinstance(data, list):
        raise ExternalAPIError("The external API returned an unexpected response.")
    posts = []
    for item in data:
        if not isinstance(item, dict) or not {"id", "title", "body"}.issubset(item):
            raise ExternalAPIError("The external API returned an unexpected response.")
        posts.append({"id": item["id"], "title": item["title"], "body": item["body"]})
    return posts
