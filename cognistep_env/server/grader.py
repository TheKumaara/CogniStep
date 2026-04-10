def grade(trajectory=None, **kwargs) -> float:
    if not trajectory:
        return 0.5

    try:
        rewards = []
        for step in trajectory:
            # Handle different formats openenv might pass trajectory in
            if isinstance(step, tuple) and len(step) == 2:
                _, obs = step
                rewards.append(getattr(obs, "reward", 0.0))
            elif hasattr(step, "reward"):
                rewards.append(step.reward)
            elif isinstance(step, dict) and "reward" in step:
                rewards.append(step["reward"])
                
        # Hackathon specified score calculation from inference.py
        score = max(0.0, min(1.0, sum(rewards) / 100.0))
        return float(score)
    except Exception:
        return 0.5
