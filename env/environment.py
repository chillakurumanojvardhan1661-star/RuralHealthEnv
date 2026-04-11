from typing import Any, Dict, List, Optional, Tuple
import random
from .models import (
    Observation, Action, Reward, State, ActionType, Resource, 
    SeverityLevel, PatientCase, PatientInfo, Vitals, ChatMessage
)
from .state import EnvironmentStateManager
from .progression import ConditionProgressionSimulator
from .reward import RewardCalculator
from .patient_generator import PatientCaseGenerator, ConversationalPatient
from .nlp_utils import InformationExtractor
from .utils import normalize_score

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
            if self.seed:
                random.seed(self.seed)
            
        patient_case = self.generator.generate_case(template_name=template_name)
        self.manager = EnvironmentStateManager(patient_case)
        
        return self._get_observation()

    def step(self, action: Action) -> Tuple[Observation, float, bool, Dict[str, Any]]:
        """Advances the environment by one step given an action."""
        if not self.manager:
            raise ValueError("Environment must be reset before calling step()")
        
        state = self.manager.get_full_state()
        if state.is_done:
            return self._get_observation(), normalize_score(0.1), True, {"error": "Episode already finished"}

        # Conversational handling
        patient_response = None
        is_question_relevant = False
        new_info_discovered = False
        was_question_asked_before = False

        if action.action_type == ActionType.ASK_QUESTION:
            # 1. Generate response
            patient_response = ConversationalPatient.generate_response(state.current_case, action.content or "")
            self.manager.add_message("assistant", action.content or "")
            self.manager.add_message("user", patient_response)
            
            # 2. Extract information
            ext_symptoms, ext_vitals = InformationExtractor.extract_info(patient_response)
            
            # Check if this info is actually new
            before_symptoms = set(state.discovered_symptoms)
            self.manager.update_discovered_data(symptoms=ext_symptoms, vitals=ext_vitals)
            after_symptoms = set(state.discovered_symptoms)
            
            if after_symptoms - before_symptoms:
                new_info_discovered = True
                
            # Simple relevance check (content matches symptoms)
            is_question_relevant = any(s.lower() in (action.content or "").lower() for s in state.current_case.symptoms)

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
            progression=progression_desc,
            new_info_discovered=new_info_discovered,
            is_question_relevant=is_question_relevant,
            was_question_asked_before=was_question_asked_before
        )
        
        # Update state
        self.manager.update_condition(new_severity, new_vitals)
        self.manager.advance_step(action, progression_desc)
        
        if is_catastrophic:
            self.manager.terminate(True)
            
        # Final decision termination
        if action.action_type in [ActionType.REFER, ActionType.TREAT, ActionType.CLASSIFY_URGENCY]:
             self.manager.terminate(True)
             
        # Detailed Info
        info = {
            "reason": progression_desc,
            "expected_action": state.current_case.correct_decision,
            "severity_level": state.current_severity,
            "resource_violation": is_catastrophic and progression_desc == "resource_violation_failure",
            "progression": progression_desc,
            "reward_breakdown": reward_obj.breakdown.model_dump(),
            "info_extracted": list(state.discovered_symptoms)
        }
        
        # Force-normalize reward as global safety net
        final_reward = normalize_score(reward_obj.score)
        state.cumulative_reward += final_reward
        
        return self._get_observation(), final_reward, state.is_done, info

    def state(self) -> State:
        """Returns the full internal state."""
        if not self.manager:
            raise ValueError("Environment must be reset before calling state()")
        return self.manager.get_full_state()

    def _get_observation(self) -> Observation:
        state = self.manager.get_full_state()
        history_msgs = state.conversation_history
        latest_utterance = history_msgs[-1].content if history_msgs else None
        
        return Observation(
            patient_info=state.current_case.patient_info,
            symptoms=list(state.discovered_symptoms), # Only show what is discovered
            vitals=state.current_vitals, 
            available_resources=self.available_resources,
            distance_to_hospital=random_distance(self.seed, state.current_case.id),
            history=[{"action": a.action_type, "content": a.content} for a in state.action_history],
            latest_utterance=latest_utterance,
            conversation_history=history_msgs,
            extracted_data={"symptoms": state.discovered_symptoms, "vitals": state.discovered_vitals}
        )

def random_distance(seed: Optional[int], case_id: str) -> int:
    import zlib
    # Deterministic distance based on case ID
    hash_val = zlib.adler32(case_id.encode())
    return (hash_val % 100) + 5 # 5km to 105km

def random_distance(seed: Optional[int], case_id: str) -> int:
    import zlib
    # Deterministic distance based on case ID
    hash_val = zlib.adler32(case_id.encode())
    return (hash_val % 100) + 5 # 5km to 105km
