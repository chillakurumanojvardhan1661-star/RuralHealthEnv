import random
import uuid
from typing import List, Dict, Any, Optional
from .models import PatientCase, PatientInfo, Vitals, SeverityLevel, UrgencyLevel, ActionType, Resource

class PatientCaseGenerator:
    TEMPLATES = [
        {
            "template_name": "T01_Dehydration_Mild",
            "symptoms": ["fatigue", "dry mouth"],
            "vitals": {"temperature": 37.0, "bp": "120/80", "heart_rate": 72},
            "severity": SeverityLevel.MILD,
            "hidden_risks": [],
            "correct_urgency": UrgencyLevel.LOW,
            "correct_decision": ActionType.TREAT,
            "required_resources": [Resource.PHC, Resource.MEDICINES],
            "progression_rate": 1.0,
            "info": {"age": 25, "gender": "male"}
        },
        {
            "template_name": "T02_Heatstroke_Severe",
            "symptoms": ["high fever", "confusion", "lack of sweating"],
            "vitals": {"temperature": 40.5, "bp": "90/60", "heart_rate": 120},
            "severity": SeverityLevel.SEVERE,
            "hidden_risks": ["hypertension"],
            "correct_urgency": UrgencyLevel.HIGH,
            "correct_decision": ActionType.REFER,
            "required_resources": [Resource.AMBULANCE, Resource.IV],
            "progression_rate": 2.0,
            "info": {"age": 60, "gender": "female"}
        },
        {
            "template_name": "T03_Abdominal_Pain_Moderate",
            "symptoms": ["abdominal pain", "nausea"],
            "vitals": {"temperature": 38.2, "bp": "110/75", "heart_rate": 88},
            "severity": SeverityLevel.MODERATE,
            "hidden_risks": ["diabetes"],
            "correct_urgency": UrgencyLevel.MEDIUM,
            "correct_decision": ActionType.DIAGNOSE,
            "required_resources": [Resource.PHC, Resource.STAFF],
            "progression_rate": 1.2,
            "info": {"age": 45, "gender": "male"}
        },
        {
            "template_name": "T04_Respiratory_Infection_Moderate",
            "symptoms": ["cough", "fever", "shortness of breath"],
            "vitals": {"temperature": 39.0, "bp": "115/70", "heart_rate": 95},
            "severity": SeverityLevel.MODERATE,
            "hidden_risks": ["asthma"],
            "correct_urgency": UrgencyLevel.MEDIUM,
            "correct_decision": ActionType.TREAT,
            "required_resources": [Resource.PHC, Resource.OXYGEN],
            "progression_rate": 1.5,
            "info": {"age": 35, "gender": "female"}
        },
        {
            "template_name": "T05_Snakebit_Severe",
            "symptoms": ["swelling", "fang marks", "dizziness"],
            "vitals": {"temperature": 37.2, "bp": "80/50", "heart_rate": 130},
            "severity": SeverityLevel.SEVERE,
            "hidden_risks": [],
            "correct_urgency": UrgencyLevel.HIGH,
            "correct_decision": ActionType.REFER,
            "required_resources": [Resource.AMBULANCE, Resource.ICU],
            "progression_rate": 2.5,
            "info": {"age": 12, "gender": "male"}
        },
        {
            "template_name": "T06_Malaria_Mild",
            "symptoms": ["shivering", "fever", "headache"],
            "vitals": {"temperature": 38.0, "bp": "110/70", "heart_rate": 80},
            "severity": SeverityLevel.MILD,
            "hidden_risks": [],
            "correct_urgency": UrgencyLevel.LOW,
            "correct_decision": ActionType.TREAT,
            "required_resources": [Resource.PHC, Resource.MEDICINES],
            "progression_rate": 1.0,
            "info": {"age": 30, "gender": "female"}
        },
        {
            "template_name": "T07_Accidental_Injury_Severe",
            "symptoms": ["bleeding", "fracture", "pain"],
            "vitals": {"temperature": 36.8, "bp": "90/50", "heart_rate": 125},
            "severity": SeverityLevel.SEVERE,
            "hidden_risks": ["blood thinners"],
            "correct_urgency": UrgencyLevel.HIGH,
            "correct_decision": ActionType.REFER,
            "required_resources": [Resource.AMBULANCE, Resource.STAFF],
            "progression_rate": 2.0,
            "info": {"age": 50, "gender": "male"}
        },
        {
            "template_name": "T08_Dengue_Moderate",
            "symptoms": ["joint pain", "fever", "skin rash"],
            "vitals": {"temperature": 39.2, "bp": "100/65", "heart_rate": 105},
            "severity": SeverityLevel.MODERATE,
            "hidden_risks": [],
            "correct_urgency": UrgencyLevel.MEDIUM,
            "correct_decision": ActionType.TREAT,
            "required_resources": [Resource.PHC, Resource.IV],
            "progression_rate": 1.4,
            "info": {"age": 22, "gender": "female"}
        },
        {
            "template_name": "T09_Childbirth_Emergency_Severe",
            "symptoms": ["premature contractions", "high BP"],
            "vitals": {"temperature": 37.1, "bp": "160/110", "heart_rate": 100},
            "severity": SeverityLevel.SEVERE,
            "hidden_risks": ["pre-eclampsia"],
            "correct_urgency": UrgencyLevel.HIGH,
            "correct_decision": ActionType.REFER,
            "required_resources": [Resource.AMBULANCE, Resource.ICU],
            "progression_rate": 1.8,
            "info": {"age": 28, "gender": "female"}
        },
        {
            "template_name": "T10_Chest_Pain_Severe",
            "symptoms": ["chest pain", "sweating", "shortness of breath"],
            "vitals": {"temperature": 36.9, "bp": "140/90", "heart_rate": 115},
            "severity": SeverityLevel.SEVERE,
            "hidden_risks": ["smoking", "diabetes"],
            "correct_urgency": UrgencyLevel.HIGH,
            "correct_decision": ActionType.REFER,
            "required_resources": [Resource.AMBULANCE, Resource.OXYGEN, Resource.ICU],
            "progression_rate": 2.2,
            "info": {"age": 55, "gender": "male"}
        }
    ]

    def __init__(self, seed: Optional[int] = None):
        if seed is not None:
            random.seed(seed)

    def generate_case(self, template_name: Optional[str] = None) -> PatientCase:
        if template_name:
            template = next((t for t in self.TEMPLATES if t["template_name"] == template_name), None)
            if not template:
                template = random.choice(self.TEMPLATES)
        else:
            template = random.choice(self.TEMPLATES)

        case_id = str(uuid.uuid4())[:8]
        
        return PatientCase(
            id=case_id,
            patient_info=PatientInfo(**template["info"]),
            symptoms=template["symptoms"],
            vitals=Vitals(**template["vitals"]),
            severity=template["severity"],
            hidden_risks=template["hidden_risks"],
            correct_urgency=template["correct_urgency"],
            correct_decision=template["correct_decision"],
            required_resources=template["required_resources"],
            progression_rate=template["progression_rate"],
            template_name=template["template_name"]
        )
