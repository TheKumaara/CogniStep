- # 🧠 OpenEnv Hackathon — Complete Professional Guide
- ## 📌 Objective
  
  Build a **real-world simulation environment** where an AI agent can interact, learn, and be evaluated using the OpenEnv framework.  
  
---
- # 1. 🧩 Core Concept
- ## What You Are Building
  
  You are **NOT building an AI model**.  
  
  You are building:  
  
  >   
  
  A **structured environment (simulation)** where an AI agent operates.  
  
---
- ## System Overview
  
  ```
  Real-world Problem
        ↓
  Environment (simulation)
        ↓
  Agent (decision maker)
        ↓
  Interaction (state → action → reward)
        ↓
  Policy (learned strategy)
  ```
  
---
- # 2. 🧠 Key Components
- ## 2.1 Environment (Primary Focus)
  
  Defines the entire system.  
- ### Must include:
- **State** → current situation
- **Action space** → what agent can do
- **Reward function** → feedback signal
- **Rules / transitions** → how system evolves
  
---
- ## 2.2 Agent
- Uses LLM or simple RL
- Observes state → takes action
- Learns via rewards
  
---
- ## 2.3 Policy
  
  Final output of learning:  
  
  ```
  Policy = function(state) → best action
  ```
  
---
- # 3. 🔁 Interaction Flow
  
  ```
  env.reset()
  ↓
  Agent observes state
  ↓
  Agent takes action
  ↓
  env.step(action)
  ↓
  Returns: next_state, reward, done
  ↓
  Repeat
  ```
  
---
- # 4. 📋 Mandatory Requirements
- ## 4.1 Real-World Simulation
- Must simulate real tasks (NOT games)
- Examples:
	- Email triage
	- Customer support
	- EdTech learning
	- Scheduling systems
	    
---
- ## 4.2 OpenEnv Interface
  
  Your environment must implement:  
  
  ```
  reset()
  step(action)
  state()
  ```
  
---
- ## 4.3 Tasks (Minimum 3)
  
  | Task | Difficulty |
  |---|---|
  | Task 1 | Easy |
  | Task 2 | Medium |
  | Task 3 | Hard |
  
  Each task must:  
- Have clear objective
- Be measurable
  
---
- ## 4.4 Grader
- Outputs score between **0.0 – 1.0**
- Must be **deterministic**
- Measures performance objectively
  
---
- ## 4.5 Reward Function
  
  Must:  
- Provide **step-wise feedback**
- Reward progress
- Penalize bad actions
  
  Example:  
  
  ```
  Correct action → +1
  Improvement → +2
  Wrong action → -1
  ```
  
---
- ## 4.6 Inference Script ( `inference.py` )
  
  Responsibilities:  
- Run agent inside environment
- Log steps in strict format
- ### Required Log Format
  
  ```
  [START] task=... env=... model=...
  [STEP] step=n action=... reward=... done=... error=...
  [END] success=... steps=n rewards=...
  ```
  
---
- ## 4.7 Deployment
- Must deploy on **Hugging Face Space**
- Must include **Dockerfile**
  
---
- # 5. 🧪 Pre-Validation Requirements
  
  All must pass:  
  
  ```
  1. HF Space responds to /reset (HTTP 200)
  2. Docker build succeeds
  3. openenv validate passes
  ```
  
---
- # 6. 🏆 Evaluation Criteria
- ## 6.1 Real-world Utility (30%)
- Practical usefulness
- Industry relevance
  
---
- ## 6.2 Task & Grader Quality (25%)
- Clear objectives
- Accurate scoring
- Difficulty progression
  
---
- ## 6.3 Environment Design (20%)
- Clean state management
- Logical actions
- Strong reward shaping
  
---
- ## 6.4 Code Quality & Spec (15%)
- OpenEnv compliance
- Docker works
- HF Space live
  
---
- ## 6.5 Creativity (10%)
- Novel problem
- Interesting mechanics
  
---
- # 7. ⚠️ Disqualification Criteria
  
  Immediate rejection if:  
- Environment does not deploy
- Docker fails
- No inference script
- Grader always returns same score
- Plagiarized solution
  
---
- # 8. 🔥 Winning Strategy
- ## DO:
- Choose **complex real-world problem**
- Design **rich environment**
- Create **strong reward function**
- Show **learning improvement**
  
---
- ## DO NOT:
- Use simple rule-based system
- Focus only on model
- Build toy examples
  
---
- # 9. 🧠 Key Insights
- ### 9.1 Environment = Product
  
  Main evaluation focus  
  
---
- ### 9.2 Agent = Tester
  
  Used only to validate environment  
  
---
- ### 9.3 Reward = Intelligence
  
  Defines learning quality  
  
---
- ### 9.4 Policy = Output
  
  What agent ultimately learns  
  
---
- # 10. 🎯 Final Summary
  
  >   
  
  You are building a **controlled simulation environment** where an AI agent interacts, learns optimal behavior, and is evaluated using structured rewards and tasks.  
  
---
- # 🚀 Execution Checklist
  
  ```
  ✔ Real-world problem selected
  ✔ Environment defined (state, action, reward)
  ✔ 3 tasks implemented
  ✔ Graders working (0–1 score)
  ✔ inference.py implemented
  ✔ Dockerfile working
  ✔ HF Space deployed
  ✔ openenv validate passes
  ✔ Pre-validation script passes
  ```
  
---
- # 💥 Final One-Line
  
  >   
  
  Build a realistic, well-defined environment where an agent can learn and be evaluated — that is the core of this hackathon.
