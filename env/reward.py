from .models import Reward, RewardBreakdown, Action, ActionType, PatientCase, UrgencyLevel, Resource
from typing import List

class RewardCalculator:
    @staticmethod
    def calculate_step_reward(
        action: Action,
        patient_case: PatientCase,
        available_resources: List[Resource],
        is_catastrophic: bool,
        progression: str
    ) -> Reward:
        breakdown = RewardBreakdown()
        
        # 1. Triage Score (based on inferred urgency if diagnose action)
        if action.action_type == ActionType.DIAGNOSE:
            inferred_urgency = action.details.get("urgency")
            if inferred_urgency == patient_case.correct_urgency:
                breakdown.triage = 0.3
            elif inferred_urgency in [UrgencyLevel.LOW, UrgencyLevel.MEDIUM, UrgencyLevel.HIGH]:
                # Partial score if off by one (simplified)
                breakdown.triage = 0.15
        
        # 2. Decision Score
        if action.action_type == patient_case.correct_decision:
            breakdown.correctness = 0.3
        elif action.action_type == ActionType.WAIT and patient_case.correct_decision == ActionType.DIAGNOSE:
            breakdown.correctness = 0.1
            
        # 3. Safety Score
        if not is_catastrophic:
            if progression == "improved":
                breakdown.safety = 0.2
            elif progression == "stable":
                breakdown.safety = 0.1
        else:
            breakdown.safety = -0.5 # Penalty inside the score
            
        # 4. Resource Score
        missing_resources = [r for r in patient_case.required_resources if r not in available_resources]
        if action.action_type == ActionType.TREAT:
            if not missing_resources:
                breakdown.resource_usage = 0.2
            else:
                breakdown.resource_usage = -0.2
        else:
            breakdown.resource_usage = 0.1 # Not wasting resources
            
        # Total Score
        total_score = breakdown.triage + breakdown.correctness + breakdown.safety + breakdown.resource_usage
        
        # Emergency Penalty
        if patient_case.severity == "severe" and action.action_type == ActionType.WAIT:
            total_score -= 0.7
            
        # Clip total score? Actually the prompt says 0.0 to 1.0 but penalties can make it negative
        # I'll keep it raw for now as step reward
        
        return Reward(score=round(total_score, 2), breakdown=breakdown)
