from .base import BaseGrader
from typing import List, Dict, Any
from ..models import Action, ActionType, PatientCase, UrgencyLevel

class EasyGrader(BaseGrader):
    URGENCY_MAP = {UrgencyLevel.LOW: 1, UrgencyLevel.MEDIUM: 2, UrgencyLevel.HIGH: 3}
    
    def evaluate(self, actions: List[Action], logs: List[Dict[str, Any]], patient_case: PatientCase) -> float:
        """Task 1: Correct classification -> 0.8, off-by-one -> 0.5, else 0.2."""
        score = 0.2
        for action in actions:
            if action.action_type == ActionType.CLASSIFY_URGENCY:
                inferred = action.details.get("urgency")
                if not inferred: continue
                
                try:
                    target_val = self.URGENCY_MAP[patient_case.correct_urgency]
                    inferred_val = self.URGENCY_MAP[UrgencyLevel(inferred)]
                    
                    diff = abs(target_val - inferred_val)
                    if diff == 0: 
                        score = 0.8
                        break
                    if diff == 1: 
                        score = 0.5
                        break
                except (KeyError, ValueError):
                    continue
        
        # Final Constraint
        assert 0 < score < 1, f"Invalid score in EasyGrader: {score}"
        return score
