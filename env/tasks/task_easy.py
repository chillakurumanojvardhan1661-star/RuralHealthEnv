from .base import BaseTask
from ..models import Observation, Action, ActionType
import random

class EasyTask(BaseTask):
    """Task 1: Urgency Classification (Easy). 1 step, focus on low/med/high triage from first description."""
    def reset(self) -> Observation:
        # Fixed set for easy: T01, T06 (Mild)
        templates = ["T01_Dehydration_Mild", "T06_Malaria_Mild"]
        if self.seed:
            random.seed(self.seed)
        template = random.choice(templates)
        return self.env.reset(seed=self.seed, template_name=template)
