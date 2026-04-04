from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, Tuple
from ..environment import RuralHealthEnv
from ..models import Observation, Action

class BaseTask(ABC):
    def __init__(self, seed: Optional[int] = None):
        self.env = RuralHealthEnv(seed=seed)
        self.seed = seed

    def reset(self) -> Observation:
        return self.env.reset(seed=self.seed)

    def step(self, action: Action) -> Tuple[Observation, float, bool, Dict[str, Any]]:
        return self.env.step(action)
