import requests
from runtime.result import RuntimeResult, STATUS_SUCCESS, STATUS_FAILURE
import time

def execute_handler(capability, appspec, runtime_memory):
    try:
        url = appspec.get("runtime", {}).get("target")
        start = time.time()
        r = requests.get(url, timeout=5)
        end = time.time()
        runtime_memory["response"] = {
            "status": r.status_code,
            "headers": dict(r.headers),
            "body_hash": hash(r.text),
            "elapsed": end - start,
        }
        return RuntimeResult(capability=capability, success=True, status=STATUS_SUCCESS, data=runtime_memory["response"])
    except Exception as e:
        return RuntimeResult(capability=capability, success=False, status=STATUS_FAILURE, errors=[str(e)])
