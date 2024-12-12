# src/agent.py
from typing import Dict, List, Optional
from datetime import datetime
import uuid

class Agent:
    def __init__(self, id: str, personality_generator=None):
        self.id = id
        self.personality_traits = {}
        self.relationships = {}  # {agent_id: relationship_score}
        self.interaction_history = []
        self._initialize_personality(personality_generator)

    def _initialize_personality(self, personality_generator):
        if personality_generator:
            self.personality_traits = personality_generator.generate_traits()
        else:
            # Default personality traits if no generator provided
            self.personality_traits = {
                "openness": 0.5,
                "conscientiousness": 0.5,
                "extraversion": 0.5,
                "agreeableness": 0.5,
                "neuroticism": 0.5
            }

    def interact_with(self, other: 'Agent', llm_client=None) -> float:
        interaction = Interaction(self, other, llm_client)
        result_score = interaction.calculate_outcome()
        self.update_relationship(other, result_score)
        self.interaction_history.append(interaction)
        return result_score

    def update_relationship(self, other: 'Agent', score: float):
        current_score = self.relationships.get(other.id, 0.0)
        # Update relationship score with weighted average
        self.relationships[other.id] = 0.7 * current_score + 0.3 * score

    def get_relationship(self, other: 'Agent') -> float:
        return self.relationships.get(other.id, 0.0)