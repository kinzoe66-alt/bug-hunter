import requests
import time

from runtime.result import (
    RuntimeResult,
    STATUS_SUCCESS,
    STATUS_FAILURE,
)

from runtime.simple_audit import (
    persist_execution,
)


def execute_handler(
    capability,
    appspec,
    runtime_memory,
):
    try:

        url = (
            appspec
            .get("runtime", {})
            .get("target")
        )

        start = time.time()

        response = requests.get(
            url,
            timeout=5,
        )

        end = time.time()

        response_data = {
            "status": response.status_code,
            "headers": dict(response.headers),
            "body_hash": hash(response.text),
            "body_length": len(response.text),
            "elapsed": end - start,
        }

        runtime_memory.set(
            "response",
            response_data,
        )

        result = RuntimeResult(
            capability=capability,
            success=True,
            status=STATUS_SUCCESS,
            data=response_data,
        )

        audit_path = persist_execution(
            capability,
            result,
        )

        print(
            f"Audit saved: "
            f"{audit_path}"
        )

        return result

    except Exception as error:

        result = RuntimeResult(
            capability=capability,
            success=False,
            status=STATUS_FAILURE,
            errors=[str(error)],
        )

        persist_execution(
            capability,
            result,
        )

        return result
