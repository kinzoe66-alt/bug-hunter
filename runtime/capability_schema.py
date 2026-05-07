from pathlib import Path

import yaml

from jsonschema import validate


SCHEMA_DIR = Path(
    "capabilities/schemas"
)


def load_capability_schema(
    capability: str
):

    schema_path = (
        SCHEMA_DIR /
        f"{capability}.schema.yaml"
    )

    if not schema_path.exists():
        return None

    with open(
        schema_path,
        "r",
        encoding="utf-8"
    ) as file:

        return yaml.safe_load(file)


def validate_capability_runtime(
    capability: str,
    runtime_config: dict
):

    schema = load_capability_schema(
        capability
    )

    if not schema:
        return

    validate(
        instance=runtime_config,
        schema=schema
    )