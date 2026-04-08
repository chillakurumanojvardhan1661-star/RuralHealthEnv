from typing import List, Dict, Any, Optional
from .models import State, PatientCase, Action, ActionType, SeverityLevel, Vitals, ChatMessage

class EnvironmentStateManager:
    def __init__(self, patient_case: PatientCase, max_steps: int = 8):
        self.state = State(
            current_case=patient_case,
            step_count=0,
            max_steps=max_steps,
            action_history=[],
            conversation_history=[
                ChatMessage(role="user", content=patient_case.initial_description)
            ] if patient_case.initial_description else [],
            current_severity=patient_case.severity,
            current_vitals=patient_case.vitals,
            discovered_symptoms=[],
            discovered_vitals={},
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

    def add_message(self, role: str, content: str):
        """Adds a message to the conversation history."""
        self.state.conversation_history.append(ChatMessage(role=role, content=content))

    def update_discovered_data(self, symptoms: Optional[List[str]] = None, vitals: Optional[Dict[str, Any]] = None):
        """Updates the agent's 'extracted' data."""
        if symptoms:
            for symptom in symptoms:
                if symptom not in self.state.discovered_symptoms:
                    self.state.discovered_symptoms.append(symptom)
        if vitals:
            self.state.discovered_vitals.update(vitals)

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
