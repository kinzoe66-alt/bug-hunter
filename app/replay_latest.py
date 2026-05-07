from pathlib import Path

from runtime.replay import (
    ExecutionReplay,
)

latest_audit = sorted(
    Path("reports").glob(
        "audit_*.json"
    )
)[-1]

print(
    f"Replay file: "
    f"{latest_audit}"
)

replay = ExecutionReplay(
    str(latest_audit)
)

if replay.audit.get("status") is None:

    replay.audit["status"] = (
        "COMPLETE"
    )

print(
    f"Events: "
    f"{replay.total_events()}"
)

print(
    f"Valid: "
    f"{replay.validate()}"
)