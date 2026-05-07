from runtime.handlers import execute_handler

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
        "handler": execute_handler,
        "description": "Deep HTTP analysis and fuzzing",
        "policy": {**DEFAULT_POLICY, "replayable": True, "requires_runtime_keys": ["response"]},
    },

    "auth_bypass_probe": {
        "handler": execute_handler,
        "description": "Authentication bypass probing",
        "policy": {**DEFAULT_POLICY, "replayable": True, "requires_runtime_keys": ["auth_response"]},
    },

    "sql_injection_detector": {
        "handler": execute_handler,
        "description": "SQL injection detection",
        "policy": {**DEFAULT_POLICY, "replayable": True, "requires_runtime_keys": ["response"]},
    },

    "xss_fuzzer": {
        "handler": execute_handler,
        "description": "Cross-site scripting fuzzing",
        "policy": {**DEFAULT_POLICY, "replayable": True, "requires_runtime_keys": ["response"]},
    },

    "session_hijack_probe": {
        "handler": execute_handler,
        "description": "Session hijacking analysis",
        "policy": {**DEFAULT_POLICY, "replayable": True, "requires_runtime_keys": ["cookies"]},
    },
}

"deep_http_analysis": {
    "handler": execute_handler,
    "description": "Deep HTTP analysis and fuzzing",
    "policy": {
        **DEFAULT_POLICY,
        "replayable": True,
        "requires_runtime_keys": [],
        "allow_skip_on_missing_dependencies": False,
    },
},
