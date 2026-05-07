from runtime.runner import run_execution_plan
from runtime.appspec_loader import load_appspec
from runtime.appspec_validator import validate_appspec, load_schema
from runtime.materializer import materialize_execution_plan

# Load schema and appspec
schema = load_schema("schemas/appspec.schema.yaml")
appspec = load_appspec("specs/deep_http_test.appspec.yaml")
validate_appspec(appspec, schema)

# Materialize execution plan
execution_plan = materialize_execution_plan(appspec)

# Run the execution plan (anomaly logging capabilities must be defined in registry)
run_execution_plan(execution_plan, appspec)
