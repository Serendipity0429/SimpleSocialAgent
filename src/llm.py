# src/llm.py
import openai
from typing import Dict, Any
import os
import re
class LLMClient:
    def __init__(self, api_key: str, model_name: str , base_url: str):
        self.api_key = api_key
        self.model_name = model_name
        self.base_url = base_url
        self.client = openai.OpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )

    def generate_response(self, prompt: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error generating response: {e}")
            return ""

    def analyze_interaction(self, context: Dict[str, Any]) -> Dict[str, float]:
        prompt = self._create_interaction_prompt(context)
        response = self.generate_response(prompt)
        return self._parse_interaction_response(response)

    def _create_interaction_prompt(self, context: Dict[str, Any]) -> str:
        '''
            context: {
                "agent_a_traits": Dict[str, float],
                "agent_a_neighbors": Dict[str, float],
                "agent_b_traits": Dict[str, float],
                "agent_b_neighbors": Dict[str, float],
                "common_friends": Dict[str, Dict[str, float]],
                "current_score": float
            }
        '''
        common_friends = context["common_friends"]
        common_friends_str = "\n".join([
            f"[{friend_id}]: Agent A score: {data['agent_a_score']}, Agent B score: {data['agent_b_score']}" for friend_id, data in common_friends.items()])
        if not len(common_friends):
            common_friends_str = "No common friends."
        agent_a_friends_str = "\n".join([
            f"[{friend_id}]: {score}" for friend_id, score in context["agent_a_neighbors"].items()])
        if not len(context["agent_a_neighbors"]):
            agent_a_friends_str = "No friends."
        agent_b_friends_str = "\n".join([
            f"[{friend_id}]: {score}" for friend_id, score in context["agent_b_neighbors"].items()])
        if not len(context["agent_b_neighbors"]):
            agent_b_friends_str = "No friends."
        # Despite redundancy in neighbor and common friends information, we include both for clarity
        prompt = f"""
        Analyze the interaction between two agents with the following traits:
        Agent A: {context['agent_a_traits']}
        Agent B: {context['agent_b_traits']}
        Current relationship score: {context['current_score']}
        Agent A has following {len(context['agent_a_neighbors'])} friends with relationship scores: {agent_a_friends_str}
        Agent B has following {len(context['agent_a_neighbors'])} friends with relationship scores: {agent_b_friends_str}
        Common friends: They have {len(common_friends)} common friends with the following scores: {common_friends_str}
        
        Please evaluate their interaction and return a new relationship score (0-1),
        considering their personality compatibility and interaction history.
        
        Your final score should be written at the end of your response in a single line in the format: "[FINAL SCORE]: <score>", where <score> is the new relationship score.
        """
        return prompt

    def _parse_interaction_response(self, response: str) -> Dict[str, float]:
        try:
            # Simple parsing - extract the first float found in the response
            scores = re.findall(r"\[FINAL SCORE\]: (\d+\.\d+)", response)
            if scores:
                return {"score": float(scores[-1])}
            return {"score": 0.5}  # Default neutral score
        except Exception:
            return {"score": 0.5}