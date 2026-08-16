from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class ExecutionState:
    """
    Canonical state for one AK Engine autonomous execution.

    Agents should gradually write their results into this state
    instead of passing unrelated values around independently.
    """

    goal: str = ""

    # Routing
    task: str = "general"

    # Current pipeline phase
    phase: str = "initialized"

    # Intelligence inputs
    research: str = ""
    memories: List[Any] = field(default_factory=list)
    plan: List[str] = field(default_factory=list)

    # Dependencies
    packages: List[str] = field(default_factory=list)

    # Generated project
    project: Dict[str, Any] = field(default_factory=dict)
    project_root: str = ""
    entrypoint: str = ""

    # Runtime
    sample_input: str = ""
    execution_result: Dict[str, Any] = field(default_factory=dict)

    # Verification / validation
    verification: Optional[Dict[str, Any]] = None
    validation_passed: Optional[bool] = None

    # Autonomous healing
    repairs: List[Dict[str, Any]] = field(default_factory=list)
    attempts: int = 0

    # Errors
    errors: List[str] = field(default_factory=list)

    # Final lifecycle state
    final_status: str = "pending"

    def set_phase(self, phase: str):
        self.phase = phase

    def add_error(self, error: Any):
        if error is None:
            return

        text = str(error)

        if text:
            self.errors.append(text)

    def add_repair(self, repair: Dict[str, Any]):
        if isinstance(repair, dict):
            self.repairs.append(repair)

    def increment_attempt(self):
        self.attempts += 1

    def succeed(self):
        self.final_status = "success"
        self.phase = "completed"

    def fail(self):
        self.final_status = "failed"
        self.phase = "failed"

    def snapshot(self) -> Dict[str, Any]:
        """
        Return a serializable view of the execution state.
        """

        return {
            "goal": self.goal,
            "task": self.task,
            "phase": self.phase,
            "research": self.research,
            "memories": self.memories,
            "plan": self.plan,
            "packages": self.packages,
            "project": self.project,
            "project_root": self.project_root,
            "entrypoint": self.entrypoint,
            "sample_input": self.sample_input,
            "execution_result": self.execution_result,
            "verification": self.verification,
            "validation_passed": self.validation_passed,
            "repairs": self.repairs,
            "attempts": self.attempts,
            "errors": self.errors,
            "final_status": self.final_status,
        }
