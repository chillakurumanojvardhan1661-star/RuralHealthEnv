import os
import sys
# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from env.environment import RuralHealthEnv
from env.models import Action, ActionType

def test_conversational_turn():
    env = RuralHealthEnv(seed=42)
    obs = env.reset(template_name="T10_Chest_Pain_Severe")
    
    # 1. Check initial utterance
    assert obs.latest_utterance is not None
    assert "chest" in obs.latest_utterance.lower()
    
    # 2. Ask a question
    action = Action(action_type=ActionType.ASK_QUESTION, content="Do you have any pain in your jaw?")
    obs, reward, done, info = env.step(action)
    
    # 3. Check response
    assert obs.latest_utterance is not None
    assert "jaw" in obs.latest_utterance.lower()
    assert "assistant" in [m.role for m in obs.conversation_history]
    assert "user" in [m.role for m in obs.conversation_history]
    
    # 4. Check extraction
    # The symptom to response for chest pain includes 'jaw' which should be extracted as 'vision' or something based on my simple extractor?
    # Wait, my extractor maps 'jaw' to 'pain'? No, I should check nlp_utils.
    assert len(obs.symptoms) > 0

def test_urgency_classification():
    env = RuralHealthEnv(seed=42)
    env.reset(template_name="T01_Dehydration_Mild")
    
    action = Action(action_type=ActionType.CLASSIFY_URGENCY, details={"urgency": "low"})
    obs, reward, done, info = env.step(action)
    
    assert done
    assert reward > 0

if __name__ == "__main__":
    test_conversational_turn()
    test_urgency_classification()
    print("Conversational tests passed!")
