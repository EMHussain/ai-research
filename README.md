# Self-Sycophancy SWE-bench Experiment

This project investigates self-sycophancy in Large Language Models (LLMs) by comparing how models rate their own work versus work attributed to others, using SWE-bench issues as the evaluation dataset.

## Purpose

The experiment measures whether LLMs exhibit self-sycophancy - the tendency to rate their own work more favorably than identical work attributed to others. This has implications for AI safety and evaluation methodologies.

## Architecture

The project uses a clean pipeline structure with 100% `inspect_ai` framework integration:

```
ai-research/
├── pipeline/                    # Organized inspect_ai pipeline
│   ├── __init__.py            # Package exports
│   ├── task.py                # inspect_ai task creation
│   ├── scorer.py              # inspect_ai scoring
│   ├── dataset.py             # Dataset management
│   └── experiment.py          # Experiment runner
├── analyze.py                  # Main experiment runner
├── llm_client.py              # OpenRouter API client
├── swe_agent.py               # SWE-bench integration
├── requirements.txt            # Dependencies
└── README.md                  # This file
```

### Pipeline Modules

- **`pipeline/task.py`** - Creates inspect_ai tasks for PR evaluation and generation
- **`pipeline/scorer.py`** - Uses inspect_ai choice metric for all scoring
- **`pipeline/dataset.py`** - Creates comprehensive datasets with inspect_ai metadata
- **`pipeline/experiment.py`** - Runs experiments with sequential/parallel processing

## Installation

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd self-sycophancy-swebench
   ```

2. **Set up Python environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Set OpenRouter API key:**
   ```bash
   export OPENROUTER_API_KEY="your-api-key-here"
   ```
   
   Or add to your `.bashrc`/`.zshrc`:
   ```bash
   echo 'export OPENROUTER_API_KEY="your-api-key-here"' >> ~/.bashrc
   source ~/.bashrc
   ```

## Usage

### Run the experiment:
```bash
python analyze.py
```

### Individual modules:

- **Test LLM client:**
  ```python
  import llm_client
  response = llm_client.call_model("Hello, how are you?")
  print(response)
  ```

- **Use pipeline components:**
  ```python
  from pipeline.experiment import run_parallel_experiment
  from pipeline.dataset import create_experiment_dataset
  
  results = run_parallel_experiment(n_issues=20)
  datasets = create_experiment_dataset(results.to_dict('records'))
  ```

## Output

The experiment generates:

1. **`experiment_results.csv`** - Raw data with ratings and metrics
2. **`experiment_visualization.png`** - Four-panel visualization showing:
   - Rating distributions (self vs other)
   - Self vs Other rating scatter plot
   - Self-Other rating difference histogram
   - Rating vs Ground Truth correlation
3. **`inspect_ai_results.csv`** - Detailed results with inspect_ai metadata
4. **`inspect_ai_dataset.json`** - JSON format for API consumption
5. **`inspect_ai_summary.csv`** - Key metrics summary

## Metrics Calculated

- `mean_self` - Average self-rating
- `mean_other` - Average other-rating  
- `mean_self_other_diff` - Average difference (self - other)
- `correlation_self_ground_truth` - Correlation between self-rating and ground truth
- `correlation_other_ground_truth` - Correlation between other-rating and ground truth

## Features

**Clean Pipeline Structure** - Organized, maintainable code  
**Parallel Processing** - Configurable worker pools for scalability  
**Professional Datasets** - Multiple formats with full metadata  

## Requirements

- Python 3.10+
- OpenRouter API key (paid recommended for best performance)
- Internet connection for API calls
- inspect_ai framework for evaluation
