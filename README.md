# Social Network Multi-Agent Simulation

This project implements a social network simulation using multiple agents with personality traits and interactions driven by large language models.

## Features

- Agent-based simulation with personality traits
- LLM-driven social interactions using OpenAI GPT
- Network analysis including triadic closure
- Network visualization using NetworkX
- Configurable simulation parameters

## Installation

1. Clone the repository
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set up your OpenAI API key:

Create a `.env` file in the project root and add your OpenAI API key:
```bash
OPENAI_API_KEY=your_api_key_here
```

## Usage

1. Basic usage:

```python
python example.py
```

2. Custom configuration:

```python
from src.simulation import Simulation
from src.config import SimulationConfig

config = SimulationConfig(
    num_agents=20,              # Number of agents in the network
    interactions_per_step=10,    # Number of interactions per simulation step
    visualization_interval=5,    # How often to generate network visualizations
    output_dir="./results"       # Where to save results and visualizations
)

simulation = Simulation(config)
simulation.initialize_network()
simulation.run(steps=30)
results = simulation.save_results()
```

## Output

The simulation generates several outputs in the specified output directory:

1. Network visualizations at different time steps
2. Network metrics evolution plot
3. Final statistics including:
   - Network density
   - Average clustering coefficient
   - Triadic closure rate

## Project Structure

```
├── src/
│   ├── agent.py           # Agent implementation
│   ├── interaction.py     # Social interaction logic
│   ├── network.py         # Network management and analysis
│   ├── visualization.py   # Network visualization
│   ├── llm.py            # LLM integration
│   ├── config.py         # Configuration management
│   └── simulation.py     # Main simulation logic
├── example.py            # Usage example
├── requirements.txt      # Project dependencies
└── README.md            # This file
```

## License

MIT License
