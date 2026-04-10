from openenv.core.env_client import EnvClient
from openenv.core.client_types import StepResult

try:
    from .models import EdTechAction, EdTechObservation, EdTechState
except ImportError:
    from models import EdTechAction, EdTechObservation, EdTechState


class EdTechEnv(EnvClient[EdTechAction, EdTechObservation, EdTechState]):
    """
    OpenEnv-compatible client for EdTech environment
    Supports:
    - HTTP mode
    - Docker mode (from_docker_image)
    """

    def _step_payload(self, action: EdTechAction) -> dict:
        return {
            "action_type": action.action_type
        }

    def _parse_result(self, payload: dict) -> StepResult:
        observation = EdTechObservation(
            knowledge=payload.get("knowledge", 0.0),
            attention=payload.get("attention", 0.0),
            fatigue=payload.get("fatigue", 0.0),
            difficulty=payload.get("difficulty", 1),
            step=payload.get("step", 0),
            reward=payload.get("reward", 0.0),
            done=payload.get("done", False),
        )

        return StepResult(
            observation=observation,
            reward=payload.get("reward", 0.0),
            done=payload.get("done", False),
        )

    def _parse_state(self, payload: dict) -> EdTechState:
        return EdTechState(
            knowledge=payload.get("knowledge", 0.0),
            attention=payload.get("attention", 0.0),
            fatigue=payload.get("fatigue", 0.0),
            difficulty=payload.get("difficulty", 1),
            step=payload.get("step", 0),
        )