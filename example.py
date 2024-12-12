# example.py
import os
from src.simulation import Simulation
from src.config import SimulationConfig
from src.llm import LLMClient

def main():
    # Configure simulation
    config = SimulationConfig(
        num_agents=10,
        interactions_per_step=5,
        visualization_interval=5,
        output_dir="./simulation_results",
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )
    
    # Initialize LLM client if API key is available
    if config.openai_api_key:
        llm_client = LLMClient(config.openai_api_key, config.model_name)
        config.llm_client = llm_client
    else:
        print("Warning: No OpenAI API key provided. Using basic interaction model.")
        config.llm_client = None
    
    # Create and run simulation
    simulation = Simulation(config)
    simulation.initialize_network()
    
    # Run simulation for 20 steps
    simulation.run(steps=20)
    
    # Save and analyze results
    results = simulation.save_results()
    
    # Print final statistics
    print("\nFinal Network Statistics:")
    for metric, value in results["final_stats"].items():
        print(f"{metric}: {value:.3f}")

if __name__ == "__main__":
    main()
pip install openai networkx matplotlib
export OPENAI_API_KEY='your-api-key'
