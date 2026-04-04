from .base import BaseGrader
from typing import List, Dict, Any
from ..models import Action, ActionType, PatientCase, Resource

class MediumGrader(BaseGrader):
    def evaluate(self, actions: List[Action], logs: List[Dict[str, Any]], patient_case: PatientCase) -> float:
        """Task 2: Correct decision -> 1.0, invalid (resource violation) -> 0.0, else 0.2 partial if waiting."""
        if not actions: return 0.0
        
        # Check for catastrophic survival
        any_catastrophic = any(log.get("resource_violation") or log.get("reason") == "critical_deterioration" for log in logs if log)
        if any_catastrophic:
            return 0.0
        
        final_action = actions[-1]
        
        if final_action.action_type == patient_case.correct_decision:
            return 1.0
        
        if final_action.action_type == ActionType.WAIT or final_action.action_type == ActionType.DIAGNOSE:
            return 0.2
            
        return 0.0
