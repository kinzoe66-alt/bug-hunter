RULES = {

    "unexpected_status": lambda response: (
        response.get("status_code") != 200
    ),

    "server_header_exposed": lambda response: (
        "Server" in response.get(
            "headers",
            {}
        )
    ),

    "missing_content_type": lambda response: (
        "Content-Type" not in response.get(
            "headers",
            {}
        )
    )
}


def analyze_response(
    response: dict,
    enabled_rules: list
):

    findings = []

    for rule_name in enabled_rules:

        rule = RULES.get(rule_name)

        if not rule:
            continue

        if rule(response):
            findings.append(rule_name)

    return {
        "valid": len(findings) == 0,
        "findings": findings
    }