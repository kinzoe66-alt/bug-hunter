import json
from pathlib import Path

from capabilities.registry import (
    CAPABILITY_REGISTRY,
)

from runtime.lifecycle import (
    validate_lifecycle_transition,
)

VALID_AUDIT_STATUSES = {
    "COMPLETE",
    "FAILED",
    "DEGRADED",
}


class ExecutionReplay:

    def __init__(self, audit_path: str):
        self.audit_path = Path(audit_path)
        self.audit = self._load()

    def _load(self):
        with open(self.audit_path, "r", encoding="utf-8") as file:
            return json.load(file)

    def events(self):
        for event in self.audit.get("events", []):
            yield event

    def total_events(self):
        return len(self.audit.get("events", []))

    def validate_lifecycle(self):

        status = self.audit.get("status")

        if status is None:
            self.audit["status"] = "COMPLETE"
            status = "COMPLETE"

        if status not in VALID_AUDIT_STATUSES:
            raise ValueError(
                f"Invalid audit status: {status}"
            )

        if self.total_events() == 0:
            raise ValueError(
                f"{status} audit has no events"
            )

        if status == "DEGRADED":

            has_failure = any(
                isinstance(
                    event.get("result"),
                    dict
                )
                and (
                    event["result"].get("success")
                    is False
                )
                for event in self.events()
            )

            if not has_failure:

                raise ValueError(
                    "Degraded audit "
                    "has no failed result"
                )

        return True

    def validate_dependencies(self):

        reconstructed_memory = set()

        for event in self.events():

            capability = event.get("capability")

            result = event.get("result", {})

            capability_config = (
                CAPABILITY_REGISTRY.get(
                    capability
                )
            )

            if not capability_config:

                raise ValueError(
                    f"Unknown capability: "
                    f"{capability}"
                )

            policy = capability_config.get(
                "policy",
                {}
            )

            required_keys = policy.get(
                "requires_runtime_keys",
                []
            )

            if result.get("status") == "SKIPPED":

                allow_skip = policy.get(
                    "allow_skip_on_missing_dependencies",
                    False
                )

                if not allow_skip:

                    raise ValueError(
                        f"Illegal SKIPPED state: "
                        f"{capability}"
                    )

                missing = [
                    key
                    for key in required_keys
                    if key not in reconstructed_memory
                ]

                if not missing:

                    raise ValueError(
                        "SKIPPED without "
                        "missing dependencies: "
                        f"{capability}"
                    )

                continue

            missing = [
                key
                for key in required_keys
                if key not in reconstructed_memory
            ]

            if missing:

                if result.get("success") is not False:

                    raise ValueError(
                        "Replay dependency "
                        "violation not reflected: "
                        f"{missing}"
                    )

            if result.get("success") is True:

                if capability == "auth_validation":
                    reconstructed_memory.add(
                        "response"
                    )

                if capability == "security_scan":
                    reconstructed_memory.add(
                        "analysis"
                    )

        return True

    def validate_transitions(self):

        final_status = self.audit.get(
            "status",
            "COMPLETE"
        )

        observed_status = "RUNNING"

        degraded_seen = False

        for event in self.events():

            result = event.get("result", {})

            if (
                result.get("success") is False
            ):

                capability = event.get(
                    "capability"
                )

                capability_config = (
                    CAPABILITY_REGISTRY.get(
                        capability,
                        {}
                    )
                )

                policy = capability_config.get(
                    "policy",
                    {}
                )

                failure_mode = policy.get(
                    "failure_mode"
                )

                allow_continuation = (
                    policy.get(
                        "allow_degraded_continuation",
                        False
                    )
                )

                if (
                    failure_mode
                    == "RECOVERABLE"
                    and allow_continuation
                ):

                    validate_lifecycle_transition(
                        observed_status,
                        "DEGRADED"
                    )

                    observed_status = (
                        "DEGRADED"
                    )

                    degraded_seen = True

                    continue

                validate_lifecycle_transition(
                    observed_status,
                    "FAILED"
                )

                observed_status = "FAILED"

                break

        if observed_status != "FAILED":

            validate_lifecycle_transition(
                observed_status,
                final_status
            )

        if (
            degraded_seen
            and final_status != "COMPLETE"
        ):

            raise ValueError(
                "Degraded execution "
                "did not complete legally"
            )

        return True

    def validate(self):

        self.validate_lifecycle()

        self.validate_dependencies()

        self.validate_transitions()

        return True
