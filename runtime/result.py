from dataclasses import dataclass, field
from typing import Any
import time


STATUS_SUCCESS = "SUCCESS"
STATUS_FAILURE = "FAILURE"
STATUS_RETRY_EXHAUSTED = "RETRY_EXHAUSTED"
STATUS_SKIPPED = "SKIPPED"


@dataclass
class RuntimeResult:

    capability: str
    success: bool
    status: str
    data: Any = None
    errors: list = field(default_factory=list)
    timestamp: float = field(default_factory=time.time)

    def to_dict(self):

        return {
            "capability": self.capability,
            "success": self.success,
            "status": self.status,
            "data": self.data,
            "errors": self.errors,
            "timestamp": self.timestamp,
        }
