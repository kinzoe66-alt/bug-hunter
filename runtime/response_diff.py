def compare_responses(
    baseline,
    mutated,
):

    differences = {}

    for key in [
        "status",
        "body_hash",
        "body_length",
    ]:

        if baseline.get(key) != mutated.get(key):

            differences[key] = {
                "baseline": baseline.get(key),
                "mutated": mutated.get(key),
            }

    baseline_headers = (
        baseline.get("headers", {})
    )

    mutated_headers = (
        mutated.get("headers", {})
    )

    added_headers = []

    for header in mutated_headers:

        if header not in baseline_headers:
            added_headers.append(header)

    removed_headers = []

    for header in baseline_headers:

        if header not in mutated_headers:
            removed_headers.append(header)

    if added_headers:

        differences["added_headers"] = (
            added_headers
        )

    if removed_headers:

        differences["removed_headers"] = (
            removed_headers
        )

    baseline_time = baseline.get(
        "elapsed",
        0,
    )

    mutated_time = mutated.get(
        "elapsed",
        0,
    )

    timing_delta = abs(
        mutated_time - baseline_time
    )

    if timing_delta > 0.5:

        differences["timing_delta"] = {
            "baseline": baseline_time,
            "mutated": mutated_time,
        }

    return differences
