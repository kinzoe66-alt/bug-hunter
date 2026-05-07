from adapters.http_adapter import send_request

from runtime.analyzer import analyze_response
from runtime.reporter import generate_report
from runtime.result import RuntimeResult, STATUS_SUCCESS, STATUS_FAILURE
from runtime.memory import RuntimeMemory


def execute_handler(
    capability: str,
    app_spec: dict,
    runtime_memory: RuntimeMemory
):

    runtime_config = app_spec.get(
        "runtime",
        {}
    )

    handlers = {

        "route_analysis": lambda: "interpreting input",

        "auth_validation": lambda: runtime_memory.set(
            "response",
            send_request(
                runtime_config["target"]
            )
        ),

        "security_scan": lambda: runtime_memory.set(
            "analysis",
            analyze_response(
                runtime_memory.require(
                    "response"
                ),
                runtime_config[
                    "analysis_rules"
                ]
            )
        ),

        "reporting": lambda: generate_report(
            runtime_memory.require(
                "analysis"
            ),
            app_spec
        ),
    }

    handler = handlers.get(
        capability
    )

    if not handler:

        return RuntimeResult(
            capability=capability,
            success=False,
            status=STATUS_FAILURE,
            errors=[
                f"Unknown capability: {capability}"
            ],
        )

    try:

        return RuntimeResult(
            capability=capability,
            success=True,
            status=STATUS_SUCCESS,
            data=handler(),
        )

    except Exception as error:

        return RuntimeResult(
            capability=capability,
            success=False,
            status=STATUS_FAILURE,
            errors=[
                str(error)
            ],
        )