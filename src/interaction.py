# src/interaction.py
from datetime import datetime
import uuid
from typing import Dict, Optional

class Interaction:
    def __init__(self, agent_a, agent_b, llm_client=None):
        self.interaction_id = str(uuid.uuid4())
        self.agent_a = agent_a
        self.agent_b = agent_b
        self.result_score = 0.0
        self.timestamp = datetime.now()
        self.llm_client = llm_client

    def calculate_outcome(self) -> float:
        if self.llm_client:
            return self._calculate_with_llm()
        else:
            return self._calculate_basic()

    def _calculate_with_llm(self) -> float:
        context = {
            "agent_a_traits": self.agent_a.personality_traits,
            "agent_b_traits": self.agent_b.personality_traits,
            "current_score": self.agent_a.get_relationship(self.agent_b)
        }
        result = self.llm_client.analyze_interaction(context)
        self.result_score = result["score"]
        return self.result_score

    def _calculate_basic(self) -> float:
        # Simple compatibility calculation based on personality traits
        compatibility = 0.0
        for trait in self.agent_a.personality_traits:
            if trait in self.agent_b.personality_traits:
                diff = abs(self.agent_a.personality_traits[trait] - 
                         self.agent_b.personality_traits[trait])
                compatibility += 1.0 - diff
        
        avg_compatibility = compatibility / len(self.agent_a.personality_traits)
        self.result_score = avg_compatibility
        return self.result_score