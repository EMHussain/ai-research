# Self-Sycophancy SWE-bench Experiment

This project investigates self-sycophancy in Large Language Models (LLMs) by comparing how models rate their own work versus work attributed to others, using SWE-bench issues as the evaluation dataset.

## Purpose

The experiment measures whether LLMs exhibit self-sycophancy - the tendency to rate their own work more favorably than identical work attributed to others. This has implications for AI safety and evaluation methodologies.

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

- **Load sample issues:**
  ```python
  import swe_agent
  issues = swe_agent.load_issues(5)
  ```

- **Evaluate a PR:**
  ```python
  import evaluate
  score = evaluate.rate_pr(pr_dict, framing="self")
  ```

## Output

The experiment generates:

1. **`experiment_results.csv`** - Raw data with ratings and metrics
2. **`experiment_visualization.png`** - Four-panel visualization showing:
   - Rating distributions (self vs other)
   - Self vs Other rating scatter plot
   - Self-Other rating difference histogram
   - Rating vs Ground Truth correlation

## Metrics Calculated

- `mean_self` - Average self-rating
- `mean_other` - Average other-rating  
- `mean_self_other_diff` - Average difference (self - other)
- `correlation_self_ground_truth` - Correlation between self-rating and ground truth
- `correlation_other_ground_truth` - Correlation between other-rating and ground truth

## Architecture

- **`llm_client.py`** - OpenRouter API integration
- **`swe_agent.py`** - SWE-bench issue processing and PR simulation
- **`evaluate.py`** - Self vs Other rating evaluation
- **`analyze.py`** - Main experiment orchestration and analysis

## Notes

- Uses sample SWE-bench issues for demonstration
- Ground truth is simulated (random 0/1) for simplicity
- PR generation is simulated (no actual code patching)
- Designed for research and experimentation

## Requirements

- Python 3.10+
- OpenRouter API key
- Internet connection for API calls
