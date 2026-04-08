import random
import uuid
from typing import List, Dict, Any, Optional
from .models import PatientCase, PatientInfo, Vitals, SeverityLevel, UrgencyLevel, ActionType, Resource

class PatientCaseGenerator:
    TEMPLATES = [
        {
            "template_name": "T01_Dehydration_Mild",
            "initial_description": "Namaste, I am feeling very tired since yesterday... my mouth feels very dry.",
            "symptoms": ["fatigue", "dry mouth"],
            "symptoms_to_responses": {
                "fever": "No, I don't think I have a fever, just very thirsty.",
                "pain": "Not much pain, just feeling very weak.",
                "dizzy": "Yes, a little bit when I stand up."
            },
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
            "initial_description": "Help... my father is very hot to touch and he is talking strangely... he was in the fields all day.",
            "symptoms": ["high fever", "confusion", "lack of sweating"],
            "symptoms_to_responses": {
                "breathing": "His breathing is very fast and shallow.",
                "conscious": "He is awake but he doesn't know where he is.",
                "water": "He is not able to drink anything, he is too confused."
            },
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
            "initial_description": "I have a lot of pain in my stomach... it started after lunch.",
            "symptoms": ["abdominal pain", "nausea"],
            "symptoms_to_responses": {
                "vomit": "I feel like I am going to vomit, but nothing comes out.",
                "fever": "I feel a bit warm, but it's mostly the pain.",
                "diarrhea": "No, that is not an issue right now."
            },
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
            "initial_description": "My daughter has a bad cough and she says she can't breathe properly.",
            "symptoms": ["cough", "fever", "shortness of breath"],
            "symptoms_to_responses": {
                "noise": "Yes, there is a whistling sound when she breathes.",
                "chest": "She says her chest feels very tight.",
                "sleep": "She couldn't sleep at all last night because of the coughing."
            },
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
            "initial_description": "Something bit me in the dark... my leg is swelling up very fast and I feel dizzy.",
            "symptoms": ["swelling", "fang marks", "dizziness"],
            "symptoms_to_responses": {
                "look": "I see two small dots on my ankle, it's turning blue.",
                "vision": "Everything is looking a bit blurry now.",
                "pain": "It burns like fire, I can't even stand on it."
            },
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
            "initial_description": "I have been shivering and having high fever every few hours.",
            "symptoms": ["shivering", "fever", "headache"],
            "symptoms_to_responses": {
                "body": "My whole body aches, especially my joints.",
                "appetite": "I don't feel like eating anything, only want to drink water.",
                "chills": "Yes, the shivering is so bad I need three blankets."
            },
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
            "initial_description": "Pranam, my son fell from the tractor... he is bleeding a lot from his leg.",
            "symptoms": ["bleeding", "fracture", "pain"],
            "symptoms_to_responses": {
                "bone": "I think I see the bone sticking out, it's very scary.",
                "pale": "He is looking very pale and his hands are cold.",
                "conscious": "He is crying loudly, so he is awake."
            },
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
            "initial_description": "My joints are hurting so much I can't move... and I have a red rash on my arms.",
            "symptoms": ["joint pain", "fever", "skin rash"],
            "symptoms_to_responses": {
                "eyes": "It hurts behind my eyes when I look at the light.",
                "gum": "My gums bled a little bit when I brushed this morning.",
                "flu": "It feels like a very bad flu, but the pain is different."
            },
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
            "initial_description": "My wife is 8 months pregnant and she has severe headache and her feet are very swollen.",
            "symptoms": ["premature contractions", "high BP"],
            "symptoms_to_responses": {
                "vision": "She says she is seeing spots in front of her eyes.",
                "stomach": "She has pain in the upper part of her stomach too.",
                "baby": "The baby was moving many times earlier, but now it's quiet."
            },
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
            "initial_description": "I have a heavy feeling in my chest... it feels like an elephant is sitting on me.",
            "symptoms": ["chest pain", "sweating", "shortness of breath"],
            "symptoms_to_responses": {
                "jaw": "The pain is going up into my jaw and left arm.",
                "sweat": "Yes, I am sweating even though it is not hot today.",
                "nausea": "I feel a bit sick in my stomach too."
            },
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
            template_name=template["template_name"],
            initial_description=template["initial_description"],
            symptoms_to_responses=template["symptoms_to_responses"]
        )

class ConversationalPatient:
    @staticmethod
    def generate_response(patient_case: PatientCase, agent_question: str) -> str:
        """Generates a realistic rural response based on keywords in the agent's question."""
        agent_question = agent_question.lower()
        
        # Check for specific symptom keywords
        for keyword, response in patient_case.symptoms_to_responses.items():
            if keyword in agent_question:
                return response
        
        # Generic vague responses if no keyword matches
        vague_responses = [
            "I don't know exactly... it just feels wrong.",
            "It started a few hours ago and now it's getting worse.",
            "I am just very worried about what is happening.",
            "Could you repeat that? I didn't understand the big words.",
            "Yes, my family is also worried, please help us."
        ]
        return random.choice(vague_responses)
