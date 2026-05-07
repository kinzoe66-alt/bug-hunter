AppSpec = {

    "name": "api_security_probe",

    "intent": "analyze API behavior for inconsistencies",

    "target": None,

    "workflow": [
        "INTERPRET",
        "PROBE",
        "COMPARE",
        "EVALUATE",
        "COMPLETE"
    ],

    "tools": [
        "request_sender",
        "response_analyzer",
        "report_generator"
    ],

    "analysis_rules": [
        "unexpected_status",
        "server_header_exposed",
        "missing_content_type"
    ],

    "constraints": {
        "deterministic": True,
        "trace": True,
        "parallel_safe": True
    }
}