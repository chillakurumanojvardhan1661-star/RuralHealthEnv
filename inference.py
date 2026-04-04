import os
import json
import sys
import traceback
import warnings
from typing import List, Dict, Any, Optional

# Suppress Pydantic and other warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.simplefilter("ignore")
from openai import OpenAI
from env.tasks.task_easy import EasyTask
from env.tasks.task_medium import MediumTask
from env.tasks.task_hard import HardTask
from env.models import Action, ActionType
from env.graders.grader_easy import EasyGrader
from env.graders.grader_medium import MediumGrader
from env.graders.grader_hard import HardGrader

# Configuration from environment variables
API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4-turbo")
HF_TOKEN = os.getenv("HF_TOKEN", "")

client = OpenAI(api_key=HF_TOKEN or os.getenv("OPENAI_API_KEY", "EMPTY"), base_url=API_BASE_URL)

def get_llm_action(observation: Dict[str, Any]) -> Action:
    prompt = f"""
    You are an AI medical agent working in a rural clinic in India. 
    Your goal is to decide the best course of action for the patient based on symptoms, vitals, and available resources.
    
    Observation:
    {json.dumps(observation, indent=2)}
    
    Choose one action type: 'diagnose', 'treat', 'refer', or 'wait'.
    - If you choose 'diagnose', you MUST provide an 'urgency' level in 'details' (low, medium, high).
    - If you choose 'treat', you assume local facility has the resources.
    - If you choose 'refer', you send the patient to a higher hospital.
    - If you choose 'wait', you observe the patient for another step.
    
    Return your decision STICKTLY as a JSON object:
    {{
        "action_type": "diagnose|treat|refer|wait",
        "details": {{ "urgency": "low|medium|high", "reasoning": "..." }}
    }}
    """
    
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "system", "content": "You are a medical healthcare agent."},
                      {"role": "user", "content": prompt}],
            response_format={ "type": "json_object" }
        )
        content = response.choices[0].message.content
        data = json.loads(content)
        return Action(action_type=ActionType(data["action_type"]), details=data.get("details", {}))
    except Exception as e:
        # Fallback to wait on error
        return Action(action_type=ActionType.WAIT, details={"error": str(e)})

def run_task(task_name: str):
    tasks_map = {
        "easy": (EasyTask(seed=42), EasyGrader()),
        "medium": (MediumTask(seed=42), MediumGrader()),
        "hard": (HardTask(seed=42), HardGrader())
    }
    
    if task_name not in tasks_map:
        return

    task, grader = tasks_map[task_name]
    obs = task.reset()
    
    print(f"[START] task={task_name} env=RuralHealthEnv model={MODEL_NAME}")
    
    step_num = 0
    done = False
    rewards = []
    actions = []
    logs = []
    
    try:
        while not done and step_num < 8:
            step_num += 1
            action = get_llm_action(obs.model_dump())
            actions.append(action)
            
            obs, reward, done, info = task.step(action)
            rewards.append(reward)
            logs.append(info)
            
            reward_str = f"{reward:.2f}"
            done_str = "true" if done else "false"
            error_str = "null"
            
            print(f"[STEP] step={step_num} action={action.action_type.value} reward={reward_str} done={done_str} error={error_str}")
            
            if task_name == "easy": # Easy is single step
                done = True

        # Calculate success based on grader
        final_score = grader.evaluate(actions, logs, task.env.state().current_case)
        success = "true" if final_score >= 0.1 else "false"
        rewards_list = ",".join([f"{r:.2f}" for r in rewards])
        
        print(f"[END] success={success} steps={step_num} rewards={rewards_list}")
        
    except Exception as e:
        error_msg = str(e).replace("\n", " ")
        print(f"[STEP] step={step_num+1} action=null reward=0.00 done=true error={error_msg}")
        print(f"[END] success=false steps={step_num} rewards=0.00")

if __name__ == "__main__":
    for task in ["easy", "medium", "hard"]:
        run_task(task)
