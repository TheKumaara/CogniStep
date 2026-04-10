import asyncio
import os
from typing import List, Optional

from openai import OpenAI

from cognistep_env.client import EdTechEnv
from cognistep_env.models import EdTechAction


# ----------------------------
# CONFIG
# ----------------------------

IMAGE_NAME = os.getenv("IMAGE_NAME", "cognistep_env")

API_KEY = os.getenv("HF_TOKEN") or os.getenv("API_KEY")
API_BASE_URL = os.getenv("API_BASE_URL") or "https://openrouter.ai/api/v1"
MODEL_NAME = os.getenv("MODEL_NAME") or "qwen/qwen3.6-plus:free"

TASK_NAME = "cognistep"
BENCHMARK = "cognistep_env"

MAX_STEPS = 20
SUCCESS_THRESHOLD = 0.3


# ----------------------------
# LOGGING (MANDATORY)
# ----------------------------

def log_start(task: str, env: str, model: str):
    print(f"[START] task={task} env={env} model={model}", flush=True)


def log_step(step: int, action: str, reward: float, done: bool, error: Optional[str]):
    error_val = error if error else "null"
    done_val = str(done).lower()

    print(
        f"[STEP] step={step} action={action} reward={reward:.2f} done={done_val} error={error_val}",
        flush=True,
    )


def log_end(success: bool, steps: int, score: float, rewards: List[float]):
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    success_str = str(success).lower()
    print(
        f"[END] success={success_str} steps={steps} rewards={rewards_str} score={score:.3f}",
        flush=True,
    )


# ----------------------------
# LLM AGENT
# ----------------------------

def choose_action(client: OpenAI, obs) -> str:
    prompt = f"""
You are an AI teacher.

Student state:
knowledge={obs.knowledge}
attention={obs.attention}
fatigue={obs.fatigue}
difficulty={obs.difficulty}

Choose best action:
teach, quiz, revise, increase_difficulty, decrease_difficulty

ONLY return action.
"""

    try:
        res = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are an expert AI teacher."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
            max_tokens=5,
        )

        action = (res.choices[0].message.content or "").strip().lower()

        valid = [
            "teach",
            "quiz",
            "revise",
            "increase_difficulty",
            "decrease_difficulty",
        ]

        return action if action in valid else "teach"

    except Exception as e:
        print(f"[DEBUG] LLM error: {e}", flush=True)
        return "teach"


# ----------------------------
# MAIN LOOP
# ----------------------------

async def main():

    client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)

    rewards: List[float] = []
    steps_taken = 0
    score = 0.0
    success = False

    log_start(task=TASK_NAME, env=BENCHMARK, model=MODEL_NAME)

    # 🔥 Docker-based environment (official way)
    env = await EdTechEnv.from_docker_image(IMAGE_NAME, ports={8000: 8000})

    try:
        result = await env.reset()        
        obs = result.observation

        for step in range(1, MAX_STEPS + 1):

            if result.done:
                break

            action_str = choose_action(client, obs)

            result = await env.step(
                EdTechAction(action_type=action_str)
            )

            reward = result.reward or 0.0
            done = result.done
            error = None
            obs = result.observation

            rewards.append(reward)
            steps_taken = step

            log_step(step, action_str, reward, done, error)

            if done:
                break

        score = max(0.0, min(1.0, sum(rewards) / 100))
        success = score >= SUCCESS_THRESHOLD

    finally:
        try:
            await env.close()
        except Exception as e:
            print(f"[DEBUG] env.close() error: {e}", flush=True)

        log_end(success, steps_taken, score, rewards)


if __name__ == "__main__":
    asyncio.run(main())