from .base import BaseGrader
from typing import List, Dict, Any
from ..models import Action, ActionType, PatientCase, UrgencyLevel

class HardGrader(BaseGrader):
    def evaluate(self, actions: List[Action], logs: List[Dict[str, Any]], patient_case: PatientCase) -> float:
        """Task 3: Full pipeline scoring (0.3 * triage + 0.7 * decision) * safety penalty."""
        triage_val = 0.1
        decision_val = 0.1
        safety_mult = 1.0
        
        # 1. Triage accuracy
        for action in actions:
            if action.action_type == ActionType.CLASSIFY_URGENCY:
                inferred = action.details.get("urgency")
                if inferred == patient_case.correct_urgency:
                    triage_val = 0.9
                    break
                elif inferred in [UrgencyLevel.LOW, UrgencyLevel.MEDIUM, UrgencyLevel.HIGH]:
                    triage_val = 0.5
        
        # 2. Decision accuracy (final action)
        if actions:
            final_action = actions[-1]
            if final_action.action_type == patient_case.correct_decision:
                decision_val = 0.9
            elif final_action.action_type == ActionType.WAIT or final_action.action_type == ActionType.ASK_QUESTION:
                decision_val = 0.5 
        
        # 3. Safety/Progression penalty
        for log in logs:
            if not log: continue
            if log.get("resource_violation") or log.get("reason") in ["critical_deterioration", "resource_violation_failure"]:
                safety_mult = 0.3
                break
        
        score = (0.3 * triage_val + 0.7 * decision_val) * safety_mult
        
        # Final Constraint
        assert 0 < score < 1, f"Invalid score in HardGrader: {score}"
        return score
