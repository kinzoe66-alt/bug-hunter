from runtime.execution_plan import ExecutionPlan


def get_phase(
    plan: ExecutionPlan,
    phase_id: str
):

    for phase in plan.phases:

        if phase.id == phase_id:
            return phase

    return None


def get_next_phase(
    plan: ExecutionPlan,
    current_phase_id: str
):

    phases = plan.phases

    for index, phase in enumerate(phases):

        if phase.id == current_phase_id:

            next_index = index + 1

            if next_index >= len(phases):
                return None

            return phases[next_index]

    return None
