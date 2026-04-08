from enum import Enum
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field

class ActionType(str, Enum):
    DIAGNOSE = "diagnose"
    TREAT = "treat"
    REFER = "refer"
    WAIT = "wait"
    ASK_QUESTION = "ask_question"
    CLASSIFY_URGENCY = "classify_urgency"
    RESPOND = "respond"

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

class ChatMessage(BaseModel):
    role: str  # "assistant" (agent) or "user" (patient)
    content: str

class Observation(BaseModel):
    patient_info: PatientInfo
    symptoms: List[str]
    vitals: Vitals
    available_resources: List[Resource]
    distance_to_hospital: int  # in km
    history: List[Dict[str, Any]]
    latest_utterance: Optional[str] = None
    conversation_history: List[ChatMessage] = Field(default_factory=list)
    extracted_data: Dict[str, Any] = Field(default_factory=dict)

class Action(BaseModel):
    action_type: ActionType
    content: Optional[str] = None
    details: Dict[str, Any] = Field(default_factory=dict)

class RewardBreakdown(BaseModel):
    safety: float = 0.0
    correctness: float = 0.0
    resource_usage: float = 0.0
    triage: float = 0.0
    question_quality: float = 0.0
    information_gain: float = 0.0

class Reward(BaseModel):
    score: float  # -1.0 to 1.0
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
    initial_description: str = ""
    symptoms_to_responses: Dict[str, str] = Field(default_factory=dict)

class State(BaseModel):
    current_case: PatientCase
    step_count: int
    max_steps: int
    action_history: List[Action]
    conversation_history: List[ChatMessage]
    current_severity: SeverityLevel
    current_vitals: Vitals
    discovered_symptoms: List[str]
    discovered_vitals: Dict[str, Any]
    is_done: bool
    cumulative_reward: float
    last_progression: str = "stable"  # improved, worsened, stable
