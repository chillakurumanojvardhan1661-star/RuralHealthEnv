from abc import ABC, abstractmethod
from typing import List, Dict, Any
from ..models import Action, PatientCase

class BaseGrader(ABC):
    @abstractmethod
    def evaluate(self, actions: List[Action], logs: List[Dict[str, Any]], patient_case: PatientCase) -> float:
        """Returns a deterministic score between 0.0 and 1.0."""
        pass
