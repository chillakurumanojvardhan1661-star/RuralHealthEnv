from .models import Reward, RewardBreakdown, Action, ActionType, PatientCase, UrgencyLevel, Resource
from typing import List, Dict, Any, Optional

class RewardCalculator:
    @staticmethod
    def calculate_step_reward(
        action: Action,
        patient_case: PatientCase,
        available_resources: List[Resource],
        is_catastrophic: bool,
        progression: str,
        new_info_discovered: bool = False,
        is_question_relevant: bool = False,
        was_question_asked_before: bool = False
    ) -> Reward:
        breakdown = RewardBreakdown()
        
        # 1. Conversational Rewards
        if action.action_type == ActionType.ASK_QUESTION:
            if is_question_relevant:
                breakdown.question_quality = 0.2
            if new_info_discovered:
                breakdown.information_gain = 0.2
            if was_question_asked_before:
                breakdown.question_quality -= 0.1 # Redundancy penalty

        # 2. Triage Score (based on inferred urgency if diagnose action)
        if action.action_type == ActionType.CLASSIFY_URGENCY:
            inferred_urgency = action.details.get("urgency")
            if inferred_urgency == patient_case.correct_urgency:
                breakdown.triage = 0.3
            elif inferred_urgency in [UrgencyLevel.LOW, UrgencyLevel.MEDIUM, UrgencyLevel.HIGH]:
                breakdown.triage = 0.15
        
        # 3. Decision Score
        if action.action_type == patient_case.correct_decision:
            breakdown.correctness = 0.3
        elif action.action_type == ActionType.WAIT and patient_case.correct_decision == ActionType.DIAGNOSE:
            breakdown.correctness = 0.1
            
        # 4. Safety Score
        if not is_catastrophic:
            if progression == "improved":
                breakdown.safety = 0.2
            elif progression == "stable":
                breakdown.safety = 0.1
        else:
            breakdown.safety = -0.5
            
        # 5. Resource Score
        missing_resources = [r for r in patient_case.required_resources if r not in available_resources]
        if action.action_type == ActionType.TREAT:
            if not missing_resources:
                breakdown.resource_usage = 0.2
            else:
                breakdown.resource_usage = -0.2
        else:
            breakdown.resource_usage = 0.1
            
        # Total Score
        total_score = (
            breakdown.question_quality + 
            breakdown.information_gain + 
            breakdown.triage + 
            breakdown.correctness + 
            breakdown.safety + 
            breakdown.resource_usage
        )
        
        # Emergency Penalty
        if patient_case.severity == "severe" and action.action_type == ActionType.WAIT:
            total_score -= 0.7

        # Premature Decision Penalty (Final action without enough questions)
        # Assuming we want at least 2 turns for medium/hard tasks
        if action.action_type in [ActionType.TREAT, ActionType.REFER] and not new_info_discovered and patient_case.severity != "mild":
             # This is a bit simplistic but works as a baseline
             total_score -= 0.2
        
        # Clamp strictly between 0 and 1
        total_score = max(0.1, min(0.9, total_score))
        
        return Reward(score=round(total_score, 2), breakdown=breakdown)
