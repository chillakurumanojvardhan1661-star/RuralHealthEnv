from .base import BaseTask
from ..models import Observation
import random

class HardTask(BaseTask):
    """Task 3: Full Pipeline (Hard). Multi-step severe cases. 8 turns allowed for dialogue support."""
    def reset(self) -> Observation:
        # Severe cases
        templates = ["T02_Heatstroke_Severe", "T05_Snakebit_Severe", "T07_Accidental_Injury_Severe", "T09_Childbirth_Emergency_Severe", "T10_Chest_Pain_Severe"]
        if self.seed:
            random.seed(self.seed)
        template = random.choice(templates)
        return self.env.reset(seed=self.seed, template_name=template)
