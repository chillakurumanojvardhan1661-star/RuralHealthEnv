from typing import List, Dict, Any, Tuple, Optional

class InformationExtractor:
    SYMPTOM_KEYWORDS = {
        "fever": ["fever", "hot", "warm", "shiver"],
        "pain": ["pain", "hurt", "ache", "burn"],
        "breathing": ["breathe", "shortness of breath", "tight", "suffocating"],
        "vision": ["see", "vision", "eyes", "blurry", "spots"],
        "bleeding": ["blood", "bleeding", "cut"],
        "conscious": ["awake", "talking", "know where", "confused"],
        "joint_pain": ["joint", "knee", "elbow", "move"],
        "stomach": ["stomach", "abdominal", "vomit", "nausea"],
        "chest": ["chest", "heavy", "elephant", "heart"],
        "sweating": ["sweat", "perspiring"]
    }

    @staticmethod
    def extract_info(text: str) -> Tuple[List[str], Dict[str, Any]]:
        """
        Simulates extracting symptoms and vitals from text.
        Returns: (extracted_symptoms, extracted_vitals)
        """
        text = text.lower()
        extracted_symptoms = []
        extracted_vitals = {}
        
        for symptom, keywords in InformationExtractor.SYMPTOM_KEYWORDS.items():
            if any(kw in text for kw in keywords):
                extracted_symptoms.append(symptom)
        
        # Simulated vitals extraction (very simple keyword based)
        if "bp" in text or "blood pressure" in text:
             # Just a flag that it was mentioned
             extracted_vitals["bp_mentioned"] = True
             
        return extracted_symptoms, extracted_vitals
