import json
import time
import uuid


def generate_report(
    analysis: dict,
    app_spec: dict
):

    runtime_config = app_spec.get(
        "runtime",
        {}
    )

    report = {
        "id": str(uuid.uuid4()),
        "timestamp": time.time(),
        "target": runtime_config.get("target"),
        "analysis": analysis,
    }

    filename = (
        f"reports/report_{report['id']}.json"
    )

    with open(filename, "w") as file:
        json.dump(
            report,
            file,
            indent=2
        )

    return report
