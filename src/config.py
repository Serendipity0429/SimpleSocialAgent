# src/config.py
from dataclasses import dataclass
from typing import Optional

@dataclass
class SimulationConfig:
    num_agents: int = 10
    interactions_per_step: int = 5
    visualization_interval: int = 10
    output_dir: str = "./output"
    
    # LLM Configuration
    openai_api_key: Optional[str] = None
    model_name: str = "gpt-3.5-turbo"
    
    # Simulation parameters
    random_seed: int = 42
    
    def __post_init__(self):
        import os
        os.makedirs(self.output_dir, exist_ok=True)
