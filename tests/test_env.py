import os
import sys
# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from env.environment import RuralHealthEnv
from env.models import Action, ActionType, UrgencyLevel

def test_basic_lifecycle():
    env = RuralHealthEnv(seed=42)
    obs = env.reset()
    assert obs.patient_info is not None
    assert len(obs.symptoms) > 0
    
    # Take a diagnose action
    action = Action(action_type=ActionType.DIAGNOSE, details={"urgency": "medium"})
    obs, reward, done, info = env.step(action)
    
    assert reward >= -1.0 # arbitrary base
    assert not done # diagnosis shouldn't end episode unless catastrophic
    assert "reason" in info

def test_easy_task():
    from env.tasks.task_easy import EasyTask
    task = EasyTask(seed=42)
    obs = task.reset()
    assert "Mild" in task.env.state().current_case.template_name

def test_catastrophic_failure():
    from env.environment import RuralHealthEnv
    from env.models import Action, ActionType, SeverityLevel, Vitals
    
    env = RuralHealthEnv(seed=42)
    env.reset(template_name="T02_Heatstroke_Severe") # Severe
    
    # Wait in severe case -> catastrophic
    action = Action(action_type=ActionType.WAIT)
    obs, reward, done, info = env.step(action)
    
    assert done
    assert info["reason"] == "critical_deterioration"
    assert reward < 0

if __name__ == "__main__":
    test_basic_lifecycle()
    test_easy_task()
    test_catastrophic_failure()
    print("Basic tests passed!")
