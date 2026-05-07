"deep_http_analysis": {
    "handler": execute_handler,
    "description": "Deep HTTP analysis and fuzzing",
    "policy": {
        **DEFAULT_POLICY,
        "replayable": True,
    },
},from runtime.handlers import execute_handler


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

    "route_analysis": {
        "handler": execute_handler,
        "description": "Initial request interpretation",
        "policy": {
            **DEFAULT_POLICY,
        },
    },

    "auth_validation": {
        "handler": execute_handler,
        "description": "Authentication validation probe",
        "policy": {
            **DEFAULT_POLICY,
            "retry_on_failure": True,
            "max_retries": 1,
            "failure_mode": "RECOVERABLE",
            "allow_degraded_continuation": True,
        },
    },

    "security_scan": {
        "handler": execute_handler,
        "description": "Security analysis execution",
        "policy": {
            **DEFAULT_POLICY,
            "requires_runtime_keys": [
                "response",
            ],
            "allow_skip_on_missing_dependencies": True,
        },
    },

    "reporting": {
        "handler": execute_handler,
        "description": "Runtime report generation",
        "policy": {
            **DEFAULT_POLICY,
            "replayable": False,
            "requires_runtime_keys": [
                "analysis",
            ],
            "allow_skip_on_missing_dependencies": True,
        },
    },
}

# High-value bug-hunter capabilities
"deep_http_analysis": {
    "handler": execute_handler,
    "description": "Deep HTTP analysis and fuzzing",
    "policy": {
        **DEFAULT_POLICY,
        "replayable": True,
        "requires_runtime_keys": ["response"],
    },
},

"auth_bypass_probe": {
    "handler": execute_handler,
    "description": "Probe for authentication bypass vulnerabilities",
    "policy": {
        **DEFAULT_POLICY,
        "replayable": True,
        "requires_runtime_keys": ["auth_response"],
    },
},

"sql_injection_detector": {
    "handler": execute_handler,
    "description": "Detect potential SQL injection points",
    "policy": {
        **DEFAULT_POLICY,
        "replayable": True,
        "requires_runtime_keys": ["response"],
    },
},

"xss_fuzzer": {
    "handler": execute_handler,
    "description": "Cross-site scripting input fuzzing",
    "policy": {
        **DEFAULT_POLICY,
        "replayable": True,
        "requires_runtime_keys": ["response"],
    },
},

"session_hijack_probe": {
    "handler": execute_handler,
    "description": "Detect session hijacking vulnerabilities",
    "policy": {
        **DEFAULT_POLICY,
        "replayable": True,
        "requires_runtime_keys": ["cookies"],
    },
},
