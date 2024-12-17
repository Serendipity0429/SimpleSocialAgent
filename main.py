# example.py
import os
from src.simulation import Simulation
from src.config import SimulationConfig
from src.llm import LLMClient
from dotenv import load_dotenv
import argparse
import time

def parse_args():
    parser = argparse.ArgumentParser(description="Run network simulation")
    parser.add_argument("--num_agents", type=int, default=10, help="Number of agents in the network")
    parser.add_argument("--interaction_ratio_per_step", type=int, default=0.3, help="Number of interactions per simulation step (1 means full update)")
    parser.add_argument("--visualization_interval", type=int, default=1, help="Interval for visualizing network state")
    parser.add_argument("--steps", type=int, default=20, help="Number of simulation steps to run")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for simulation")
    parser.add_argument("--initial_weight", type=float, default=0.2, help="Initial edge weight for network")
    parser.add_argument("--threshold", type=float, default=0.3, help="Threshold for interaction score")
    parser.add_argument("--output_dir", type=str, default=r"D:\Personal\Computer Science\homework\网络群体与市场\agent\simulation_results", help="Output directory for saving simulation results")
    return parser.parse_args()

def main(args):
    # Load environment variables from .env file
    load_dotenv(verbose=True)
    
    # Fetch current time in the format: YYYY-MM-DD-HH-MM-SS
    current_time = time.strftime("%Y-%m-%d-%H-%M-%S")
    output_dir = args.output_dir + f"/{current_time}"
    
    # Configure simulation
    config = SimulationConfig(
        num_agents=args.num_agents,
        interaction_ratio_per_step=args.interaction_ratio_per_step,
        visualization_interval=args.visualization_interval,
        output_dir=output_dir,
        api_key=os.getenv("API_KEY"),
        base_url=os.getenv("LLM_BASE_URL"),
        model_name=os.getenv("MODEL_NAME"),
        random_seed=args.seed,
        initial_weight=args.initial_weight,
        threshold=args.threshold,
        steps=args.steps
    )
    
    # Initialize LLM client if API key is available
    if config.api_key:
        llm_client = LLMClient(config.api_key, config.model_name, config.base_url)
        config.llm_client = llm_client
    else:
        print("Warning: No API key provided. Using basic interaction model.")
        config.llm_client = None
    
    # Create and run simulation
    simulation = Simulation(config)
    simulation.initialize_network(initial_weight=config.initial_weight)
    
    # Run simulation 
    simulation.run(steps=config.steps)
    
    # Save and analyze results
    results = simulation.save_results()
    
    # Print final statistics
    print("\nFinal Network Statistics:")
    for metric, value in results["final_stats"].items():
        print(f"{metric}: {value:.3f}")

if __name__ == "__main__":
    main(parse_args())