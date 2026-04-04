from enum import Enum
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field

class ActionType(str, Enum):
    DIAGNOSE = "diagnose"
    TREAT = "treat"
    REFER = "refer"
    WAIT = "wait"

class UrgencyLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class SeverityLevel(str, Enum):
    MILD = "mild"
    MODERATE = "moderate"
    SEVERE = "severe"

class Resource(str, Enum):
    PHC = "PHC"
    MEDICINES = "medicines"
    STAFF = "staff"
    AMBULANCE = "ambulance"
    ICU = "ICU"
    OXYGEN = "oxygen"
    IV = "IV"

class PatientInfo(BaseModel):
    age: int
    gender: str

class Vitals(BaseModel):
    temperature: float
    bp: str  # e.g., "120/80"
    heart_rate: int

class Observation(BaseModel):
    patient_info: PatientInfo
    symptoms: List[str]
    vitals: Vitals
    available_resources: List[Resource]
    distance_to_hospital: int  # in km
    history: List[Dict[str, Any]]

class Action(BaseModel):
    action_type: ActionType
    details: Dict[str, Any] = Field(default_factory=dict)

class RewardBreakdown(BaseModel):
    safety: float = 0.0
    correctness: float = 0.0
    resource_usage: float = 0.0
    triage: float = 0.0

class Reward(BaseModel):
    score: float  # 0.0 to 1.0
    breakdown: RewardBreakdown

class PatientCase(BaseModel):
    id: str
    patient_info: PatientInfo
    symptoms: List[str]
    vitals: Vitals
    severity: SeverityLevel
    hidden_risks: List[str]
    correct_urgency: UrgencyLevel
    correct_decision: ActionType
    required_resources: List[Resource]
    progression_rate: float  # multiplier for deterioration
    template_name: str

class State(BaseModel):
    current_case: PatientCase
    step_count: int
    max_steps: int
    action_history: List[Action]
    current_severity: SeverityLevel
    current_vitals: Vitals
    is_done: bool
    cumulative_reward: float
    last_progression: str = "stable"  # improved, worsened, stable
