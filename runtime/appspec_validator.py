from pathlib import Path

import yaml

from jsonschema import validate

from capabilities.registry import (
    CAPABILITY_REGISTRY,
)

from runtime.capability_schema import (
    validate_capability_runtime,
)


SUPPORTED_APPSPEC_VERSIONS = {
    "0.1",
}


def load_schema(path: str) -> dict:

    with open(
        Path(path),
        "r",
        encoding="utf-8"
    ) as file:

        return yaml.safe_load(file)


def validate_appspec_version(
    appspec: dict
):

    version = appspec["appspec"]["version"]

    if version not in (
        SUPPORTED_APPSPEC_VERSIONS
    ):

        raise ValueError(
            f"Unsupported AppSpec version: "
            f"{version}"
        )


def validate_phase_capabilities(
    appspec: dict
):

    allowed = set(
        appspec["capabilities"]["allowed"]
    )

    registry_capabilities = set(
        CAPABILITY_REGISTRY.keys()
    )

    runtime_config = appspec.get(
        "runtime",
        {}
    )

    unknown_allowed = (
        allowed - registry_capabilities
    )

    if unknown_allowed:

        raise ValueError(
            f"Capabilities missing from "
            f"registry: "
            f"{sorted(unknown_allowed)}"
        )

    for phase in appspec["workflow"]["phases"]:

        for capability in phase["activates"]:

            if capability not in allowed:

                raise ValueError(
                    f"Unknown capability: "
                    f"{capability}"
                )

            if capability not in (
                registry_capabilities
            ):

                raise ValueError(
                    f"Capability not registered: "
                    f"{capability}"
                )

            validate_capability_runtime(
                capability,
                runtime_config
            )


def validate_phase_requirements(
    appspec: dict
):

    phases = appspec["workflow"]["phases"]

    phase_ids = {
        phase["id"]
        for phase in phases
    }

    for phase in phases:

        for requirement in phase.get(
            "requires",
            []
        ):

            if requirement not in phase_ids:

                raise ValueError(
                    f"Unknown phase requirement: "
                    f"{requirement}"
                )


def validate_appspec(
    appspec: dict,
    schema: dict
) -> None:

    validate(
        instance=appspec,
        schema=schema
    )

    validate_appspec_version(
        appspec
    )

    validate_phase_capabilities(
        appspec
    )

    validate_phase_requirements(
        appspec
    )