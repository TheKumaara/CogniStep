import uvicorn
from openenv.core.env_server import create_app

try:
    from ..models import EdTechAction, EdTechObservation
    from .environment import EdTechEnvironment
except ImportError:
    from models import EdTechAction, EdTechObservation
    from server.environment import EdTechEnvironment


app = create_app(
    env=EdTechEnvironment,
    action_cls=EdTechAction,
    observation_cls=EdTechObservation,
)

# =========================
# 🔥 REQUIRED FOR VALIDATOR
# =========================

def main():
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()