from runtime.http_client import (
    perform_request,
)

from runtime.response_diff import (
    compare_responses,
)


url = "https://example.com"


mutations = {

    "baseline": {},

    "x_forwarded_host": {
        "X-Forwarded-Host": "evil.com",
    },

    "x_forwarded_for": {
        "X-Forwarded-For": "127.0.0.1",
    },

    "origin_spoof": {
        "Origin": "https://evil.com",
    },

    "referer_spoof": {
        "Referer": "https://evil.com",
    },

    "content_type_json": {
        "Content-Type": "application/json",
    },
}


baseline = perform_request(
    url,
)


for name, headers in mutations.items():

    mutated = perform_request(
        url,
        headers=headers,
    )

    differences = compare_responses(
        baseline,
        mutated,
    )

    print("\n====================")
    print(name.upper())
    print("====================")

    print("\nHEADERS:")
    print(headers)

    print("\nDIFFERENCES:")
    print(differences)
