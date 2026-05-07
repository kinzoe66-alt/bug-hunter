from runtime.appspec_loader import load_appspec

from runtime.appspec_validator import (
    load_schema,
    validate_appspec,
)

from runtime.materializer import (
    materialize_execution_plan,
)

from runtime.runner import run_execution_plan


APPSPEC_PATH = "specs/api_security.appspec.yaml"
SCHEMA_PATH = "schemas/appspec.schema.yaml"


appspec = load_appspec(APPSPEC_PATH)

schema = load_schema(SCHEMA_PATH)

validate_appspec(
    appspec,
    schema
)

execution_plan = materialize_execution_plan(
    appspec
)

run_execution_plan(
    execution_plan,
    appspec
)
