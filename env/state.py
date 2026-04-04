from typing import List, Dict, Any, Optional
from .models import State, PatientCase, Action, ActionType, SeverityLevel, Vitals

class EnvironmentStateManager:
    def __init__(self, patient_case: PatientCase, max_steps: int = 8):
        self.state = State(
            current_case=patient_case,
            step_count=0,
            max_steps=max_steps,
            action_history=[],
            current_severity=patient_case.severity,
            current_vitals=patient_case.vitals,
            is_done=False,
            cumulative_reward=0.0
        )

    def advance_step(self, action: Action, progression: str):
        """Advances the internal state by one step."""
        self.state.step_count += 1
        self.state.action_history.append(action)
        self.state.last_progression = progression
        
        # Check termination
        if self.state.step_count >= self.state.max_steps:
            self.state.is_done = True
        
        # Progression logic will update severity and vitals based on action quality
        # This will be called externally to provide the progression string

    def update_condition(self, new_severity: SeverityLevel, new_vitals: Vitals):
        """Updates the current severity and vitals of the patient."""
        self.state.current_severity = new_severity
        self.state.current_vitals = new_vitals

    def terminate(self, final: bool = True):
        """Forces the episode to end."""
        self.state.is_done = final

    def get_full_state(self) -> State:
        """Returns the full internal state object."""
        return self.state
