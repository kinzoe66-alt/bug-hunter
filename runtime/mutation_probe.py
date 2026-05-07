from runtime.result import RuntimeResult, STATUS_SUCCESS, STATUS_FAILURE
from runtime.http_client import send_request
import time

def execute_handler(capability, appspec, runtime_memory):
    """
    Mutation Probe: tests for common HTTP header and payload injections.
    """
    try:
        url = appspec.get("runtime", {}).get("target")
        start = time.time()
        response = send_request(url)
        end = time.time()

        # Store results in runtime memory
        runtime_memory.set("response", {
            "status": response.status_code,
            "headers": dict(response.headers),
            "body_hash": hash(response.text),
            "elapsed": end - start,
        })

        return RuntimeResult(
            capability=capability,
            success=True,
            status=STATUS_SUCCESS,
            data=runtime_memory.get("response")
        )
    except Exception as e:
        return RuntimeResult(
            capability=capability,
            success=False,
            status=STATUS_FAILURE,
            errors=[str(e)]
        )
