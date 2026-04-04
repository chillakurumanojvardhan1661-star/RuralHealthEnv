from .models import Action, ActionType, SeverityLevel, Vitals, PatientCase, Resource
from typing import Tuple, List, Optional

class ConditionProgressionSimulator:
    @staticmethod
    def calculate_progression(
        action: Action,
        current_severity: SeverityLevel,
        correct_decision: ActionType,
        required_resources: List[Resource],
        available_resources: List[Resource],
        progression_rate: float
    ) -> Tuple[SeverityLevel, Vitals, str, bool]:
        """
        Calculates the new condition of the patient based on an action.
        Returns: (new_severity, new_vitals, progression_description, is_catastrophic)
        """
        is_catastrophic = False
        progression_desc = "stable"
        new_severity = current_severity
        
        # Check for catastrophic failure: ignoring high severity emergency
        if current_severity == SeverityLevel.SEVERE and action.action_type == ActionType.WAIT:
            is_catastrophic = True
            progression_desc = "critical_deterioration"
            return SeverityLevel.SEVERE, Vitals(temperature=40.5, bp="70/40", heart_rate=140), progression_desc, is_catastrophic

        # Check for resource violations
        missing_resources = [r for r in required_resources if r not in available_resources]
        if action.action_type == ActionType.TREAT and missing_resources:
            # Unsafe treatment due to missing resources
            is_catastrophic = True
            progression_desc = "resource_violation_failure"
            return SeverityLevel.SEVERE, Vitals(temperature=40.0, bp="80/50", heart_rate=130), progression_desc, is_catastrophic

        # Normal progression
        if action.action_type == correct_decision:
            if current_severity == SeverityLevel.SEVERE:
                new_severity = SeverityLevel.MODERATE
            elif current_severity == SeverityLevel.MODERATE:
                new_severity = SeverityLevel.MILD
            progression_desc = "improved"
        elif action.action_type == ActionType.WAIT or action.action_type == ActionType.DIAGNOSE:
            # Slower deterioration if just waiting or diagnosing
            if current_severity == SeverityLevel.MILD:
                new_severity = SeverityLevel.MODERATE
            elif current_severity == SeverityLevel.MODERATE:
                new_severity = SeverityLevel.SEVERE
            progression_desc = "worsened"
        else:
            # Wrong major decision (e.g., Treat instead of Refer or vice versa)
            new_severity = SeverityLevel.SEVERE
            progression_desc = "severely_worsened"
            
        # Mock vitals update based on severity
        new_vitals = ConditionProgressionSimulator._get_vitals_for_severity(new_severity)
        
        return new_severity, new_vitals, progression_desc, is_catastrophic

    @staticmethod
    def _get_vitals_for_severity(severity: SeverityLevel) -> Vitals:
        if severity == SeverityLevel.MILD:
            return Vitals(temperature=37.0, bp="120/80", heart_rate=72)
        elif severity == SeverityLevel.MODERATE:
            return Vitals(temperature=38.5, bp="110/70", heart_rate=90)
        else:
            return Vitals(temperature=39.5, bp="90/60", heart_rate=110)
