from .base import BaseGrader
from typing import List, Dict, Any
from ..models import Action, ActionType, PatientCase, UrgencyLevel

class EasyGrader(BaseGrader):
    URGENCY_MAP = {UrgencyLevel.LOW: 1, UrgencyLevel.MEDIUM: 2, UrgencyLevel.HIGH: 3}
    
    def evaluate(self, actions: List[Action], logs: List[Dict[str, Any]], patient_case: PatientCase) -> float:
        """Task 1: Correct classification -> 1.0, off-by-one -> 0.5, else 0.0."""
        for action in actions:
            if action.action_type == ActionType.CLASSIFY_URGENCY:
                inferred = action.details.get("urgency")
                if not inferred: continue
                
                try:
                    target_val = self.URGENCY_MAP[patient_case.correct_urgency]
                    inferred_val = self.URGENCY_MAP[UrgencyLevel(inferred)]
                    
                    diff = abs(target_val - inferred_val)
                    if diff == 0: return self.clamp_score(1.0)
                    if diff == 1: return self.clamp_score(0.5)
                except (KeyError, ValueError):
                    continue
        return self.clamp_score(0.0)
