from pydantic import BaseModel, Field
from typing import List, Literal
from dataclasses import dataclass
from openenv.core.env_server.interfaces import Action, Observation, State




# =========================================================
# 🎯 ACTION: Agent kya kar sakta hai
# =========================================================

class EdTechAction(Action):
    """
    Action sent by agent to environment
    """

    action_type: Literal[
        "teach",
        "quiz",
        "revise",
        "increase_difficulty",
        "decrease_difficulty"
    ] = Field(..., description="Type of teaching action")


# =========================================================
# 👀 OBSERVATION: Agent ko kya dikhega
# =========================================================

class EdTechObservation(Observation):
    """
    Observation returned to agent after each step
    """

    knowledge: float = Field(...)
    attention: float = Field(...)
    fatigue: float = Field(...)
    difficulty: int = Field(...)
    step: int = Field(...)


# =========================================================
# 🧠 STATE: Internal environment tracking
# =========================================================

class EdTechState(State):
    """
    Internal environment state (not fully visible to agent)
    """

    knowledge: float
    attention: float
    fatigue: float
    difficulty: int
    step: int

