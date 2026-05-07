import json
import uuid
from pathlib import Path


report = {
    "id": str(uuid.uuid4()),
    "status": "COMPLETE",
    "events": [
        {
            "capability": (
                "deep_http_analysis"
            ),
            "result": {
                "success": True,
            },
        },
    ],
}


Path("reports").mkdir(
    exist_ok=True,
)

filename = (
    "reports/audit_seed.json"
)

with open(
    filename,
    "w",
    encoding="utf-8",
) as file:

    json.dump(
        report,
        file,
        indent=2,
    )

print(filename)
