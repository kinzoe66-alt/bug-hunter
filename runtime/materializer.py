from runtime.execution_plan import (
    ExecutionPlan,
    ExecutionConstraints,
    Phase,
)


def materialize_execution_plan(appspec: dict) -> ExecutionPlan:

    phases = [
        Phase(
            id=phase["id"],
            activates=phase["activates"],
            requires=phase.get("requires", []),
        )
        for phase in appspec["workflow"]["phases"]
    ]

    constraints = ExecutionConstraints(
        ordered_execution=appspec["constraints"].get(
            "ordered_execution",
            True,
        ),
        allow_phase_skipping=appspec["constraints"].get(
            "allow_phase_skipping",
            False,
        ),
        allow_unknown_capabilities=appspec["constraints"].get(
            "allow_unknown_capabilities",
            False,
        ),
    )

    return ExecutionPlan(
        app_id=appspec["appspec"]["id"],
        version=appspec["appspec"]["version"],
        allowed_capabilities=appspec["capabilities"]["allowed"],
        phases=phases,
        constraints=constraints,
    )
