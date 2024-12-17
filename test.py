'''
    test.py: This file contains the test cases for API endpoints.
'''
import os
from dotenv import load_dotenv
from src.llm import LLMClient
from src.config import SimulationConfig

if __name__ == '__main__':
    load_dotenv()
    
    config = SimulationConfig(
        output_dir=os.getenv("OUTPUT_DIR"),
        api_key=os.getenv("API_KEY"),
        base_url=os.getenv("LLM_BASE_URL"),
        model_name=os.getenv("MODEL_NAME")
    )
    
    llm_client = LLMClient(config.api_key, config.model_name, config.base_url)
    
    while True:
        prompt = input("Enter a prompt for the LLM model (or 'exit' to quit): ")
        if prompt == 'exit':
            break
        response = llm_client.generate_response(prompt)
        print(f"LLM response: {response}")    