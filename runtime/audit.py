import json
import time
import uuid
from pathlib import Path

from runtime.lifecycle import validate_lifecycle_transition


STATUS_RUNNING = "RUNNING"
STATUS_COMPLETE = "COMPLETE"
STATUS_FAILED = "FAILED"
STATUS_DEGRADED = "DEGRADED"


class ExecutionAudit:

    def __init__(self):
        self.id = str(uuid.uuid4())
        self.started_at = time.time()
        self.completed_at = None
        self.status = STATUS_RUNNING
        self.events = []

    def record(self, phase: str, capability: str, result):
        result_data = (
            result.to_dict()
            if hasattr(result, "to_dict")
            else str(result)
        )

        self.events.append({
            "timestamp": time.time(),
            "phase": phase,
            "capability": capability,
            "result": result_data,
        })

    def complete(self):
        validate_lifecycle_transition(self.status, STATUS_COMPLETE)
        self.status = STATUS_COMPLETE
        self.completed_at = time.time()

    def fail(self):
        validate_lifecycle_transition(self.status, STATUS_FAILED)
        self.status = STATUS_FAILED
        self.completed_at = time.time()

    def degrade(self):
        validate_lifecycle_transition(self.status, STATUS_DEGRADED)
        self.status = STATUS_DEGRADED

    def summary(self):
        return {
            "id": self.id,
            "status": self.status,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "total_events": len(self.events),
            "events": self.events,
        }

    def persist(self):
        Path("reports").mkdir(exist_ok=True)

        audit = self.summary()
        filename = f"reports/audit_{self.id}.json"

        with open(filename, "w", encoding="utf-8") as file:
            json.dump(audit, file, indent=2)

        return filename
