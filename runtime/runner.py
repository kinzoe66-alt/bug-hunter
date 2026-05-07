from core.engine import SequenceEngine
from core.state import State

from runtime.phase_resolver import get_phase
from runtime.execution_plan import ExecutionPlan

from runtime.audit import (
    ExecutionAudit,
)

from runtime.memory import RuntimeMemory

from runtime.result import (
    RuntimeResult,
    STATUS_FAILURE,
    STATUS_RETRY_EXHAUSTED,
    STATUS_SKIPPED,
)

from capabilities.registry import (
    CAPABILITY_REGISTRY,
)


def run_execution_plan(
    plan: ExecutionPlan,
    app_spec: dict
):

    engine = SequenceEngine()

    audit = ExecutionAudit()

    runtime_memory = RuntimeMemory()

    initial_phase = plan.phases[0]

    state = State(
        phase=initial_phase.id,
        memory={},
        capabilities=[],
        complete=False,
    )

    while not state.complete:

        current_phase = get_phase(
            plan,
            state.phase
        )

        if not current_phase:
            break

        for capability in current_phase.activates:

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

            handler = capability_config[
                "handler"
            ]

            policy = capability_config.get(
                "policy",
                {}
            )

            retry_on_failure = policy.get(
                "retry_on_failure",
                False
            )

            max_retries = policy.get(
                "max_retries",
                0
            )

            stop_on_failure = policy.get(
                "stop_on_failure",
                True
            )

            failure_mode = policy.get(
                "failure_mode",
                "TERMINAL"
            )

            allow_degraded_continuation = (
                policy.get(
                    "allow_degraded_continuation",
                    False
                )
            )

            allow_skip = policy.get(
                "allow_skip_on_missing_dependencies",
                False
            )

            required_keys = policy.get(
                "requires_runtime_keys",
                []
            )

            missing_keys = [

                key for key in required_keys

                if runtime_memory.get(key) is None
            ]

            if missing_keys:

                if allow_skip:

                    result = RuntimeResult(
                        capability=capability,
                        success=True,
                        status=STATUS_SKIPPED,
                        errors=[
                            (
                                "Skipped missing "
                                f"dependencies: "
                                f"{missing_keys}"
                            )
                        ],
                    )

                    audit.record(
                        state.phase,
                        capability,
                        result
                    )

                    print(
                        f"[{state.phase}] "
                        f"{capability} "
                        f"-> "
                        f"{result}"
                    )

                    continue

                result = RuntimeResult(
                    capability=capability,
                    success=False,
                    status=STATUS_FAILURE,
                    errors=[
                        (
                            "Missing runtime "
                            f"dependencies: "
                            f"{missing_keys}"
                        )
                    ],
                )

                audit.record(
                    state.phase,
                    capability,
                    result
                )

                print(
                    f"[{state.phase}] "
                    f"{capability} "
                    f"-> "
                    f"{result}"
                )

                audit.fail()

                audit_path = (
                    audit.persist()
                )

                print(
                    "\nExecution failed "
                    "(DEPENDENCY_VIOLATION)."
                )

                print(
                    f"Audit saved: "
                    f"{audit_path}"
                )

                return audit.summary()

            attempt = 0

            while True:

                result = handler(
                    capability,
                    app_spec,
                    runtime_memory
                )

                audit.record(
                    state.phase,
                    capability,
                    result
                )

                print(
                    f"[{state.phase}] "
                    f"{capability} "
                    f"(attempt {attempt + 1})"
                    f" -> "
                    f"{result}"
                )

                if result.success:
                    break

                attempt += 1

                should_retry = (
                    retry_on_failure
                    and attempt <= max_retries
                )

                if should_retry:

                    print(
                        f"Retrying "
                        f"{capability}..."
                    )

                    continue

                if retry_on_failure:

                    result.status = (
                        STATUS_RETRY_EXHAUSTED
                    )

                if stop_on_failure:

                    if (
                        failure_mode
                        == "RECOVERABLE"
                    ):

                        audit.degrade()

                        if (
                            allow_degraded_continuation
                        ):

                            print(
                                "\nContinuing "
                                "under degraded "
                                "execution."
                            )

                            break

                    else:

                        audit.fail()

                    print(
                        f"\nExecution failed "
                        f"({failure_mode})."
                    )

                    audit_path = (
                        audit.persist()
                    )

                    print(
                        f"Audit saved: "
                        f"{audit_path}"
                    )

                    return audit.summary()

                break

        decision = engine.decide(state)

        state = engine.advance(
            state,
            decision,
            plan
        )

    if audit.status == "RUNNING":

        audit.complete()

    audit_path = audit.persist()

    print("\nExecution complete.")
    print(f"Audit saved: {audit_path}")

    return audit.summary()
