import json
import uuid
import time
from pathlib import Path


def persist_execution(
    capability,
    result,
):

    Path("reports").mkdir(
        exist_ok=True,
    )

    audit = {
        "id": str(uuid.uuid4()),
        "timestamp": time.time(),
        "status": "COMPLETE",
        "events": [
            {
                "capability": capability,
                "result": result.to_dict(),
            },
        ],
    }

    filename = (
        "reports/audit_"
        f"{audit['id']}.json"
    )

    with open(
        filename,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            audit,
            file,
            indent=2,
        )

    return filename
