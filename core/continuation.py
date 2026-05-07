from dataclasses import dataclass, field
from typing import List


@dataclass
class Continuation:
    id: str
    objective: str
    active: bool = True
    parent_id: str = None
    branch_type: str = None
    children: List = field(default_factory=list)