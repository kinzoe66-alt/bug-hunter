from runtime.deep_http_analysis import (
    execute_handler as deep_http_analysis_handler,
)

from runtime.mutation_probe import (
    execute_handler as mutation_probe_handler,
)

from runtime.anomaly_logger import (
    execute_handler as anomaly_logger_handler,
)


DEFAULT_POLICY = {
    "required": True,
    "stop_on_failure": True,
    "replayable": True,
    "retry_on_failure": False,
    "max_retries": 0,
    "failure_mode": "TERMINAL",
    "allow_degraded_continuation": False,
    "allow_skip_on_missing_dependencies": False,
    "requires_runtime_keys": [],
}


CAPABILITY_REGISTRY = {

    "deep_http_analysis": {
        "handler": (
            deep_http_analysis_handler
        ),
        "description": (
            "Deep HTTP analysis"
        ),
        "policy": {
            **DEFAULT_POLICY,
        },
    },

    "mutation_probe": {
        "handler": (
            mutation_probe_handler
        ),
        "description": (
            "Mutation probing"
        ),
        "policy": {
            **DEFAULT_POLICY,
        },
    },

    "anomaly_logger": {
        "handler": (
            anomaly_logger_handler
        ),
        "description": (
            "Anomaly logging"
        ),
        "policy": {
            **DEFAULT_POLICY,
            "requires_runtime_keys": [
                "response",
            ],
        },
    },
}
