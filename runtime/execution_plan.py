from dataclasses import dataclass, field
from typing import List


@dataclass
class Phase:
    id: str
    activates: List[str]
    requires: List[str] = field(default_factory=list)


@dataclass
class ExecutionConstraints:
    ordered_execution: bool = True
    allow_phase_skipping: bool = False
    allow_unknown_capabilities: bool = False


@dataclass
class ExecutionPlan:
    app_id: str
    version: str
    allowed_capabilities: List[str]
    phases: List[Phase]
    constraints: ExecutionConstraints
