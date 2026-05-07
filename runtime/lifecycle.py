ALLOWED_LIFECYCLE_TRANSITIONS = {
    "RUNNING": {"COMPLETE", "FAILED", "DEGRADED"},
    "DEGRADED": {"COMPLETE", "FAILED"},
    "COMPLETE": set(),
    "FAILED": set(),
}


def validate_lifecycle_transition(
    current_status: str,
    next_status: str
):

    allowed = ALLOWED_LIFECYCLE_TRANSITIONS.get(
        current_status,
        set()
    )

    if next_status not in allowed:

        raise ValueError(
            f"Invalid lifecycle transition: "
            f"{current_status} -> {next_status}"
        )

    return True
