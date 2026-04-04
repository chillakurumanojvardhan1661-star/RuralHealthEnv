from .base import BaseTask
from ..models import Observation

class EasyTask(BaseTask):
    """Task 1: Urgency Classification (Easy). 1 step, focus on low/med/high triage."""
    def reset(self) -> Observation:
        # Fixed set for easy: T01, T06 (Mild)
        templates = ["T01_Dehydration_Mild", "T06_Malaria_Mild"]
        import random
        if self.seed:
            random.seed(self.seed)
        template = random.choice(templates)
        return self.env.reset(seed=self.seed, template_name=template)
