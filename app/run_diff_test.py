from runtime.http_client import (
    perform_request,
)

from runtime.response_diff import (
    compare_responses,
)


url = "https://example.com"


baseline = perform_request(
    url,
)

mutated = perform_request(
    url,
    headers={
        "X-Test": "bug-hunter",
    },
)

differences = compare_responses(
    baseline,
    mutated,
)

print("\nBASELINE:")
print(baseline)

print("\nMUTATED:")
print(mutated)

print("\nDIFFERENCES:")
print(differences)
