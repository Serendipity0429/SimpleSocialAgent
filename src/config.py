# src/config.py
from dataclasses import dataclass
from typing import Optional
from .persona import PersonalityGenerator

@dataclass
class SimulationConfig:
    num_agents: int = 10
    interactions_per_step: int = 5
    visualization_interval: int = 10
    output_dir: str = "./output"
    
    # LLM Configuration
    api_key: Optional[str] = None
    model_name: str = "gpt-3.5-turbo"
    base_url: str = "https://api.openai.com"
    
    # Simulation parameters
    random_seed: int = 42
    
    # Personality Generator
    personality_generator: Optional[PersonalityGenerator] = PersonalityGenerator()
    
    # Social Simulation Parameters
    initial_weight: float = 0.2
    threshold: float = 0.3
    steps: int = 20
    
    def __post_init__(self):
        import os
        os.makedirs(self.output_dir, exist_ok=True)
    