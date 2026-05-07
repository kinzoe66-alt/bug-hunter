import requests
import time


def perform_request(
    url,
    headers=None,
):

    start = time.time()

    response = requests.get(
        url,
        headers=headers or {},
        timeout=5,
    )

    end = time.time()

    return {
        "status": response.status_code,
        "headers": dict(response.headers),
        "body_hash": hash(response.text),
        "body_length": len(response.text),
        "elapsed": end - start,
    }
