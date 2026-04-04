from typing import Any, Dict, List, Optional, Tuple
from .models import (
    Observation, Action, Reward, State, ActionType, Resource, 
    SeverityLevel, PatientCase, PatientInfo, Vitals
)
from .state import EnvironmentStateManager
from .progression import ConditionProgressionSimulator
from .reward import RewardCalculator
from .patient_generator import PatientCaseGenerator

class RuralHealthEnv:
    def __init__(self, seed: Optional[int] = None):
        self.seed = seed
        self.generator = PatientCaseGenerator(seed=seed)
        self.manager: Optional[EnvironmentStateManager] = None
        self.available_resources: List[Resource] = [
            Resource.PHC, Resource.MEDICINES, Resource.STAFF, Resource.IV
        ] # Default regional resources
        
    def reset(self, seed: Optional[int] = None, template_name: Optional[str] = None) -> Observation:
        """Resets the environment to a new patient case."""
        if seed is not None:
            self.seed = seed
            self.generator = PatientCaseGenerator(seed=seed)
            
        patient_case = self.generator.generate_case(template_name=template_name)
        self.manager = EnvironmentStateManager(patient_case)
        
        return self._get_observation()

    def step(self, action: Action) -> Tuple[Observation, float, bool, Dict[str, Any]]:
        """Advances the environment by one step given an action."""
        if not self.manager:
            raise ValueError("Environment must be reset before calling step()")
        
        state = self.manager.get_full_state()
        if state.is_done:
            return self._get_observation(), 0.0, True, {"error": "Episode already finished"}

        # Simulate progression
        new_severity, new_vitals, progression_desc, is_catastrophic = ConditionProgressionSimulator.calculate_progression(
            action=action,
            current_severity=state.current_severity,
            correct_decision=state.current_case.correct_decision,
            required_resources=state.current_case.required_resources,
            available_resources=self.available_resources,
            progression_rate=state.current_case.progression_rate
        )
        
        # Calculate Reward
        reward_obj = RewardCalculator.calculate_step_reward(
            action=action,
            patient_case=state.current_case,
            available_resources=self.available_resources,
            is_catastrophic=is_catastrophic,
            progression=progression_desc
        )
        
        # Update state
        self.manager.update_condition(new_severity, new_vitals)
        self.manager.advance_step(action, progression_desc)
        
        if is_catastrophic:
            self.manager.terminate(True)
            
        # Final decision termination
        if action.action_type in [ActionType.REFER, ActionType.TREAT]:
             self.manager.terminate(True)
             
        # Detailed Info
        info = {
            "reason": progression_desc,
            "expected_action": state.current_case.correct_decision,
            "severity_level": state.current_severity,
            "resource_violation": is_catastrophic and progression_desc == "resource_violation_failure",
            "progression": progression_desc,
            "reward_breakdown": reward_obj.breakdown.dict()
        }
        
        state.cumulative_reward += reward_obj.score
        
        return self._get_observation(), reward_obj.score, state.is_done, info

    def state(self) -> State:
        """Returns the full internal state."""
        if not self.manager:
            raise ValueError("Environment must be reset before calling state()")
        return self.manager.get_full_state()

    def _get_observation(self) -> Observation:
        state = self.manager.get_full_state()
        return Observation(
            patient_info=state.current_case.patient_info,
            symptoms=state.current_case.symptoms,
            vitals=state.current_vitals,
            available_resources=self.available_resources,
            distance_to_hospital=random_distance(self.seed, state.current_case.id),
            history=[{"action": a.action_type, "details": a.details} for a in state.action_history]
        )

def random_distance(seed: Optional[int], case_id: str) -> int:
    import zlib
    # Deterministic distance based on case ID
    hash_val = zlib.adler32(case_id.encode())
    return (hash_val % 100) + 5 # 5km to 105km
