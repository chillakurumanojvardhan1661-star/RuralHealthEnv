from .base import BaseGrader
from typing import List, Dict, Any
from ..models import Action, ActionType, PatientCase, Resource

class MediumGrader(BaseGrader):
    def evaluate(self, actions: List[Action], logs: List[Dict[str, Any]], patient_case: PatientCase) -> float:
        """Task 2: Correct decision -> 0.85, acceptable -> 0.5, else 0.15."""
        score = 0.15
        
        if actions:
            # Check for catastrophic survival
            any_catastrophic = any(log.get("resource_violation") or log.get("reason") == "critical_deterioration" for log in logs if log)
            
            if not any_catastrophic:
                final_action = actions[-1]
                if final_action.action_type == patient_case.correct_decision:
                    score = 0.85
                elif final_action.action_type == ActionType.WAIT or final_action.action_type == ActionType.DIAGNOSE:
                    score = 0.5
        
        # Final Constraint
        assert 0 < score < 1, f"Invalid score in MediumGrader: {score}"
        return score
