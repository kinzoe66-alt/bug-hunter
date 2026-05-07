from runtime.result import (
    RuntimeResult,
    STATUS_SUCCESS,
    STATUS_FAILURE,
)

from runtime.anomaly_score import (
    score_anomaly,
)


def execute_handler(
    capability,
    appspec,
    runtime_memory,
):
    try:

        response = runtime_memory.get(
            "response",
        )

        if not response:
            return RuntimeResult(
                capability=capability,
                success=False,
                status=STATUS_FAILURE,
                errors=[
                    "missing response runtime key",
                ],
            )

        differences = {}

        if (
            response.get("elapsed", 0)
            > 1
        ):
            differences[
                "timing_delta"
            ] = response[
                "elapsed"
            ]

        score = score_anomaly(
            differences,
        )

        result_data = {
            "differences": differences,
            "score": score,
        }

        runtime_memory.set(
            "anomaly_score",
            result_data,
        )

        return RuntimeResult(
            capability=capability,
            success=True,
            status=STATUS_SUCCESS,
            data=result_data,
        )

    except Exception as error:

        return RuntimeResult(
            capability=capability,
            success=False,
            status=STATUS_FAILURE,
            errors=[
                str(error),
            ],
        )
