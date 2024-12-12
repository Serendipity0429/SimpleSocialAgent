# src/llm.py
import openai
from typing import Dict, Any

class LLMClient:
    def __init__(self, api_key: str, model_name: str = "gpt-3.5-turbo"):
        self.api_key = api_key
        self.model_name = model_name
        openai.api_key = api_key

    def generate_response(self, prompt: str) -> str:
        try:
            response = openai.ChatCompletion.create(
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
        return f"""
        Analyze the interaction between two agents with the following traits:
        Agent A: {context['agent_a_traits']}
        Agent B: {context['agent_b_traits']}
        Current relationship score: {context['current_score']}
        
        Please evaluate their interaction and return a new relationship score (0-1),
        considering their personality compatibility and interaction history.
        """

    def _parse_interaction_response(self, response: str) -> Dict[str, float]:
        try:
            # Simple parsing - extract the first float found in the response
            import re
            scores = re.findall(r"0\.\d+", response)
            if scores:
                return {"score": float(scores[0])}
            return {"score": 0.5}  # Default neutral score
        except Exception:
            return {"score": 0.5}
