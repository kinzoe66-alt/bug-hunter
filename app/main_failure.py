from runtime.appspec_loader import (
    load_appspec,
)

from runtime.appspec_validator import (
    validate_appspec,
    load_schema,
)

from runtime.materializer import (
    materialize_execution_plan,
)

from runtime.runner import (
    run_execution_plan,
)


schema = load_schema(
    "schemas/appspec.schema.yaml"
)

appspec = load_appspec(
    "specs/api_security_failure.appspec.yaml"
)

validate_appspec(
    appspec,
    schema
)

execution_plan = (
    materialize_execution_plan(
        appspec
    )
)

run_execution_plan(
    execution_plan,
    appspec
)
