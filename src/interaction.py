# src/interaction.py
from datetime import datetime
import uuid
from typing import Dict, Optional
from .llm import LLMClient

class Interaction:
    def __init__(self, agent_a, agent_b, llm_client: LLMClient=None):
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
    
    def get_common_friends(self) -> Dict[str, Dict[str, float]]:
        agent_a_friends = self.agent_a.relationships
        agent_b_friends = self.agent_b.relationships
        common_friends = {}
        for friend_id in agent_a_friends:
            if friend_id in agent_b_friends:
                common_friends[friend_id] = {
                    "agent_a_score": agent_a_friends[friend_id],
                    "agent_b_score": agent_b_friends[friend_id]
                }
        return common_friends
    
    

    def _calculate_with_llm(self) -> float:
        context = {
            "agent_a_traits": self.agent_a.personality_traits,
            "agent_a_neighbors": self.agent_a.relationships,
            "agent_b_traits": self.agent_b.personality_traits,
            "agent_b_neighbors": self.agent_b.relationships,
            "common_friends": self.get_common_friends(),
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