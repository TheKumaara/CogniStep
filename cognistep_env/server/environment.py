import random 
from openenv.core.env_server.interfaces import Action, Environment, Observation

try:
    from ..models import EdTechAction, EdTechObservation, EdTechState
except ImportError:
    from models import EdTechAction, EdTechObservation, EdTechState


class EdTechEnvironment(Environment):
    def __init__(self, task_name="average_student", seed=42, **kwargs):
        super().__init__(**kwargs)
        self.max_steps = 20
        self.current_step = 0
        self.done = False
        self.task_name = task_name
        self.seed = seed
        self.rng = random.Random(self.seed)

        self._init_student()

    # ----------------------------
    # STUDENT INITIALIZATION
    # ----------------------------
    def _init_student(self):
        self.rng.seed(self.seed)
        
        if self.task_name == "strong_student":
            self.knowledge = self.rng.uniform(10, 20)
            self.attention = self.rng.uniform(0.8, 1.0)
            self.fatigue = 0.0
            self.difficulty = 1
        elif self.task_name == "weak_student":
            self.knowledge = self.rng.uniform(10, 20)
            self.attention = self.rng.uniform(0.3, 0.5)
            self.fatigue = 0.5
            self.difficulty = 3
        else: # average_student
            self.knowledge = self.rng.uniform(20, 40)
            self.attention = self.rng.uniform(0.6, 1.0)
            self.fatigue = 0.0
            self.difficulty = 3

        self.prev_knowledge = self.knowledge

    # ----------------------------
    # RESET
    # ----------------------------
    def reset(self) -> Observation:
        self.current_step = 0
        self.done = False
        self._init_student()

        return self._get_response(reward=0.0)

    # ----------------------------
    # STEP
    # ----------------------------
    def step(self, action: Action) -> Observation:
        if self.done:
            return self._get_response(0.0)

        action_type = getattr(action, "action_type", "teach")

        self.prev_knowledge = self.knowledge

        # ------------------------
        # APPLY ACTION
        # ------------------------

        if action_type == "teach":
            self._teach()

        elif action_type == "quiz":
            self._quiz()

        elif action_type == "revise":
            self._revise()

        elif action_type == "increase_difficulty":
            self.difficulty = min(10, self.difficulty + 1)

        elif action_type == "decrease_difficulty":
            self.difficulty = max(1, self.difficulty - 1)

        # ------------------------
        # ENVIRONMENT DYNAMICS
        # ------------------------

        self._apply_fatigue()
        self._apply_attention_noise()
        self._apply_forgetting()

        # ------------------------
        # REWARD
        # ------------------------

        reward = self._compute_reward(action_type)

        self.current_step += 1

        if self.current_step >= self.max_steps:
            self.done = True

        return self._get_response(reward)

    # ----------------------------
    # ACTION LOGIC
    # ----------------------------

    def _teach(self) :
        gain = self.rng.uniform(2, 5) * self.attention
        self.knowledge += gain
        self.fatigue += 0.05

    def _quiz(self):
        success_prob = self.knowledge / 100

        if self.rng.random() < success_prob:
            self.knowledge += self.rng.uniform(1, 3)
        else:
            self.knowledge -= self.rng.uniform(0.5, 1.5)

        self.fatigue += 0.08

    def _revise(self):
        self.knowledge += self.rng.uniform(1, 2)
        self.fatigue += 0.03

    # ----------------------------
    # DYNAMICS
    # ----------------------------

    def _apply_fatigue(self):
        self.fatigue = min(1.0, self.fatigue)
        self.attention -= self.fatigue * 0.1
        self.attention = max(0.3, self.attention)

    def _apply_attention_noise(self):
        noise = self.rng.uniform(-0.05, 0.05)
        self.attention = min(1.0, max(0.3, self.attention + noise))

    def _apply_forgetting(self):
        decay = 0.01 * (1 - self.attention)
        self.knowledge -= self.knowledge * decay
        self.knowledge = max(0, min(100, self.knowledge))

    # ----------------------------
    # REWARD FUNCTION (KEY PART)
    # ----------------------------

    def _compute_reward(self, action_type):

        # 📈 knowledge improvement
        knowledge_gain = self.knowledge - self.prev_knowledge

        # 🎯 difficulty alignment
        optimal_difficulty = self.knowledge / 10
        difficulty_gap = abs(self.difficulty - optimal_difficulty)

        difficulty_penalty = -0.1 * difficulty_gap

        # 😴 fatigue penalty
        fatigue_penalty = -0.2 * self.fatigue

        # 😐 boredom vs frustration
        boredom_penalty = -0.1 if self.difficulty < optimal_difficulty - 2 else 0
        frustration_penalty = -0.1 if self.difficulty > optimal_difficulty + 2 else 0

        reward = (
            knowledge_gain * 1.5
            + difficulty_penalty
            + fatigue_penalty
            + boredom_penalty
            + frustration_penalty
        )

        return float(reward)

    # ----------------------------
    # RESPONSE FORMAT
    # ----------------------------

    def _get_response(self, reward):
        return EdTechObservation(
            knowledge=round(self.knowledge, 2),
            attention=round(self.attention, 2),
            fatigue=round(self.fatigue, 2),
            difficulty=self.difficulty,
            step=self.current_step,
            reward=round(reward, 3),
            done=self.done,
        )

    # ----------------------------
    # STATE
    # ----------------------------

    @property
    def state(self) -> EdTechState:
        return EdTechState(
            knowledge=self.knowledge,
            attention=self.attention,
            fatigue=self.fatigue,
            difficulty=self.difficulty,
            step=self.current_step,
        )