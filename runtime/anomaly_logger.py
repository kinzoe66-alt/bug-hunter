import json
import uuid
from pathlib import Path


def persist_anomaly(
    mutation_name,
    headers,
    differences,
):

    Path("reports").mkdir(
        exist_ok=True,
    )

    anomaly = {
        "id": str(uuid.uuid4()),
        "mutation": mutation_name,
        "headers": headers,
        "differences": differences,
    }

    filename = (
        "reports/anomaly_"
        f"{anomaly['id']}.json"
    )

    with open(
        filename,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            anomaly,
            file,
            indent=2,
        )

    return filename
