from adapters.http_adapter import send_request

from runtime.analyzer import analyze_response
from runtime.reporter import generate_report


def execute_phase(
    phase: str,
    app_spec: dict,
    runtime_memory: dict
):

    handlers = {

        "INTERPRET": lambda: (
            "interpreting input"
        ),

        "PROBE": lambda: runtime_memory.update({
            "response": send_request(
                app_spec["target"]
            )
        }) or runtime_memory["response"],

        "COMPARE": lambda: runtime_memory.update({
            "analysis": analyze_response(
                runtime_memory["response"],
                app_spec["analysis_rules"]
            )
        }) or runtime_memory["analysis"],

        "EVALUATE": lambda: generate_report(
            runtime_memory["analysis"],
            app_spec
        ),

        "COMPLETE": lambda: (
            "execution complete"
        )
    }

    handler = handlers.get(
        phase,
        lambda: "unknown phase"
    )

    return handler()