from dataclasses import dataclass


@dataclass
class Decision:
    action: str
    reason: str