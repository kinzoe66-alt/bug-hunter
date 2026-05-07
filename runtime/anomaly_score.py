def score_anomaly(
    differences,
):

    score = 0

    if not differences:
        return score

    if (
        "status"
        in differences
    ):
        score += 5

    if (
        "body_hash"
        in differences
    ):
        score += 4

    if (
        "body_length"
        in differences
    ):
        score += 3

    if (
        "added_headers"
        in differences
    ):
        score += 2

    if (
        "removed_headers"
        in differences
    ):
        score += 2

    if (
        "timing_delta"
        in differences
    ):
        score += 1

    return score
