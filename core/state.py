from dataclasses import dataclass, field


@dataclass
class State:
    phase: str
    complete: bool

    memory: dict = field(
        default_factory=dict
    )

    capabilities: list = field(
        default_factory=list
    )
