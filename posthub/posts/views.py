"""HTTP views for the PostHub API."""

import json
from django.http import JsonResponse
from django.views.decorators.http import require_GET

from .services import ExternalAPIError, PostNotFoundError, fetch_post, fetch_posts


@require_GET
def post_list(request):
    try:
        posts = fetch_posts()
    except ExternalAPIError as exc:
        return JsonResponse({"error": str(exc)}, status=502)
    return JsonResponse({"results": posts, "count": len(posts)})


@require_GET
def post_detail(request, post_id):
    if post_id < 1:
        return JsonResponse({"error": "post_id must be a positive integer."}, status=400)
    try:
        post = fetch_post(post_id)
    except PostNotFoundError:
        return JsonResponse({"error": "Post not found."}, status=404)
    except ExternalAPIError as exc:
        return JsonResponse({"error": str(exc)}, status=502)
    return JsonResponse(post)
