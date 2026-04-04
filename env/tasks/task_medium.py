from .base import BaseTask
from ..models import Observation
import random

class MediumTask(BaseTask):
    """Task 2: Decision making (Medium). Treat or Refer based on moderate/severe cases, resource aware."""
    def reset(self) -> Observation:
        templates = ["T03_Abdominal_Pain_Moderate", "T04_Respiratory_Infection_Moderate", "T08_Dengue_Moderate"]
        if self.seed:
            random.seed(self.seed)
        template = random.choice(templates)
        return self.env.reset(seed=self.seed, template_name=template)
