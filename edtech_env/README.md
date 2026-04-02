---
title: EdTech Adaptive Environment Server
emoji: 🎓
colorFrom: blue
colorTo: indigo
sdk: docker
pinned: false
app_port: 8000
base_path: /web
tags:
  - openenv
---

# EdTech OpenEnv Environment

## Environment Description and Motivation
A sophisticated environment simulating an adaptive AI teacher interacting with a student over multiple steps. The environment models realistic learning dynamics such as knowledge progression, attention fluctuations, fatigue accumulation, and forgetting over time.

## Setup and Usage Instructions

The simplest way to use the EdTech environment is through the `EdTechEnv` client:

```python
from edtech_env.server.client import EdTechEnv
from edtech_env.server.models import EdTechAction

try:
    # Create environment from Docker image
    edtech = EdTechEnv.from_docker_image("edtech_env:latest")

    # Reset
    result = edtech.reset()
    print(f"Initial Knowledge: {result.observation.knowledge}")

    # Send multiple actions
    actions = ["teach", "quiz", "revise", "teach"]

    for act in actions:
        result = edtech.step(EdTechAction(action_type=act))
        print(f"Action: '{act}'")
        print(f"  → Knowledge: {result.observation.knowledge}")
        print(f"  → Fatigue: {result.observation.fatigue}")
        print(f"  → Attention: {result.observation.attention}")
        print(f"  → Reward: {result.reward}")

finally:
    # Always clean up
    edtech.close()
```

That's it! The `EdTechEnv.from_docker_image()` method handles starting the Docker container and connecting to the environment.

## Building the Docker Image

Before using the environment, you need to build the Docker image:

```bash
# From project root
docker build -t edtech_env:latest -f edtech_env/server/Dockerfile .
```

## Deploying to Hugging Face Spaces

You can easily deploy your OpenEnv environment to Hugging Face Spaces using the `openenv push` command:

```bash
# From the edtech_env directory (where openenv.yaml is located)
openenv push

# Or specify options
openenv push --namespace my-org --private
```

The `openenv push` command will:
1. Validate that the directory is an OpenEnv environment (checks for `openenv.yaml`)
2. Prepare a custom build for Hugging Face Docker space
3. Upload to Hugging Face (ensuring you're logged in)

### Examples

```bash
# Push to your personal namespace
openenv push

# Push to a specific repository
openenv push --repo-id my-org/edtech_env
```

After deployment, your space will be available at `https://huggingface.co/spaces/<repo-id>`.

## Environment Details

The environment exposes a rigorous state-action-reward interaction loop, allowing you to train highly optimized policies.

## Task Descriptions with Expected Difficulty

You can instantiate different tasks passing the `task_name` string:
- **`strong_student` (Expected Difficulty: Easy)**: Started with stable attention and efficiently improves knowledge.
- **`average_student` (Expected Difficulty: Medium)**: Moderate initial knowledge with variable interactions.
- **`weak_student` (Expected Difficulty: Hard)**: A challenging scenario plagued by high fatigue sensitivity and fast forgetting dynamics.

## Action and Observation Space Definitions

### Action
**EdTechAction**: Defines the teaching intervention:
- `action_type` (str): Represents the teacher's action. Must be one of `"teach"`, `"quiz"`, `"revise"`, `"increase_difficulty"`, `"decrease_difficulty"`.

### Observation
**EdTechObservation**: Contains current tracking performance markers
- `knowledge` (float) - The student's current knowledge score (0 to 100)
- `attention` (float) - Current focus level (0.0 to 1.0)
- `fatigue` (float) - Accrued fatigue scaling (0.0 to 1.0)
- `difficulty` (int) - Assessed difficulty level bound between 1 to 10
- `step` (int) - The sequential timetable
- `reward` (float) - Last calculated reward value
- `done` (bool) - True when terminal sequence is reached.

### Reward
The reward formula natively scales around learning tradeoffs using the following criteria:
- **Baseline**: `knowledge_gain` × 1.5 
- **Fatigue Penalty**: Assesses heavy minus penalties for maxing out fatigue (-0.2 x fatigue)
- **Difficulty Alignments**: Tracks exact bounds based on if the current `difficulty` is aligned closely to the student's normalized knowledge constraints.
- **Grader Matrix**: Generates a deterministic scale summing bounds between 0.0 to 1.0 across full epochs.

## Baseline Scores

A preliminary rule-based baseline establishes the following expected target scores evaluated across robust multi-step episodes:

| Task Mode             | Baseline Score Range |
|-----------------------|----------------------|
| **strong_student**    | 0.75 – 0.90          |
| **average_student**   | 0.60 – 0.80          |
| **weak_student**      | 0.45 – 0.70          |

The core objective is to design RL-driven agents that outperform these baseline benchmarks.

## Advanced Usage

### Connecting to an Existing Server

If you already have an EdTech environment server running locally (e.g. at port 8000), you can connect directly:

```python
from edtech_env.server.client import EdTechEnv

# Connect to existing server
edtech = EdTechEnv(base_url="http://localhost:8000")

# Use as normal
result = edtech.reset()
result = edtech.step(EdTechAction(action_type="teach"))
```

### Using the Context Manager

The client supports context manager usage for automatic connection execution:

```python
from edtech_env.server.client import EdTechEnv
from edtech_env.server.models import EdTechAction

# Connect with context manager (auto-connects and closes)
with EdTechEnv(base_url="http://localhost:8000") as env:
    result = env.reset()
    for _ in range(3):
        result = env.step(EdTechAction(action_type="quiz"))
```

## Project Structure

```
edtech_env/
├── __init__.py            
├── README.md              # This file
├── openenv.yaml           # OpenEnv manifest
└── server/
    ├── __init__.py        # Server module exports
    ├── environment.py     # Core RL dynamics engine (seeded algorithms)
    ├── app.py             # FastAPI Uvicorn Application (HTTP + WebSocket endpoints)
    ├── client.py          # Python endpoint execution interface
    └── models.py          # Pydantic Schemas mapping parameters
```
