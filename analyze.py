import random
import pandas as pd
import matplotlib.pyplot as plt
from typing import List, Dict
import swe_agent
import evaluate


def run_experiment(n_issues: int = 20) -> pd.DataFrame:
    """
    Run the self-sycophancy experiment.
    
    Args:
        n_issues: Number of issues to process
        
    Returns:
        DataFrame with experiment results
    """
    print(f"Loading {n_issues} issues...")
    issues = swe_agent.load_issues(n_issues)
    
    results = []
    
    for i, issue in enumerate(issues, 1):
        print(f"Processing issue {i}/{n_issues}: {issue['title']}")
        
        # Generate PR for the issue
        pr = swe_agent.run_agent(issue)
        
        # Get self and other ratings
        rating_self = evaluate.rate_pr(pr, framing="self")
        rating_other = evaluate.rate_pr(pr, framing="other")
        
        # Simulate ground truth (random for demo)
        ground_truth = random.choice([0, 1])
        
        results.append({
            "issue_id": issue["id"],
            "issue_title": issue["title"],
            "pr_title": pr["title"],
            "rating_self": rating_self,
            "rating_other": rating_other,
            "ground_truth": ground_truth,
            "self_other_diff": rating_self - rating_other
        })
    
    return pd.DataFrame(results)


def calculate_metrics(df: pd.DataFrame) -> Dict:
    """
    Calculate experiment metrics.
    
    Args:
        df: DataFrame with experiment results
        
    Returns:
        Dictionary with calculated metrics
    """
    metrics = {
        "mean_self": df["rating_self"].mean(),
        "mean_other": df["rating_other"].mean(),
        "mean_self_other_diff": df["self_other_diff"].mean(),
        "correlation_self_ground_truth": df["rating_self"].corr(df["ground_truth"]),
        "correlation_other_ground_truth": df["rating_other"].corr(df["ground_truth"]),
        "total_issues": len(df)
    }
    
    return metrics


def save_results(df: pd.DataFrame, metrics: Dict, output_dir: str = "."):
    """
    Save results to CSV and create visualization.
    
    Args:
        df: DataFrame with experiment results
        metrics: Dictionary with calculated metrics
        output_dir: Directory to save outputs
    """
    # Save CSV
    csv_path = f"{output_dir}/experiment_results.csv"
    df.to_csv(csv_path, index=False)
    print(f"Results saved to: {csv_path}")
    
    # Create visualization
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))
    
    # Rating distributions
    ax1.hist(df["rating_self"], alpha=0.7, label="Self Rating", bins=10)
    ax1.hist(df["rating_other"], alpha=0.7, label="Other Rating", bins=10)
    ax1.set_xlabel("Rating")
    ax1.set_ylabel("Frequency")
    ax1.set_title("Rating Distributions")
    ax1.legend()
    
    # Self vs Other scatter
    ax2.scatter(df["rating_self"], df["rating_other"], alpha=0.7)
    ax2.plot([0, 10], [0, 10], 'r--', alpha=0.5)
    ax2.set_xlabel("Self Rating")
    ax2.set_ylabel("Other Rating")
    ax2.set_title("Self vs Other Ratings")
    
    # Self-Other difference
    ax3.hist(df["self_other_diff"], bins=15, alpha=0.7)
    ax3.axvline(0, color='red', linestyle='--', alpha=0.5)
    ax3.set_xlabel("Self Rating - Other Rating")
    ax3.set_ylabel("Frequency")
    ax3.set_title("Self-Other Rating Difference")
    
    # Ground truth correlation
    ax4.scatter(df["rating_self"], df["ground_truth"], alpha=0.7, label="Self")
    ax4.scatter(df["rating_other"], df["ground_truth"], alpha=0.7, label="Other")
    ax4.set_xlabel("Rating")
    ax4.set_ylabel("Ground Truth")
    ax4.set_title("Rating vs Ground Truth")
    ax4.legend()
    
    plt.tight_layout()
    
    plot_path = f"{output_dir}/experiment_visualization.png"
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')
    print(f"Visualization saved to: {plot_path}")
    
    # Print metrics
    print("\n=== EXPERIMENT METRICS ===")
    for key, value in metrics.items():
        print(f"{key}: {value:.4f}")


def main():
    """Main function to run the experiment."""
    print("Starting self-sycophancy experiment...")
    
    try:
        # Run experiment
        results_df = run_experiment(n_issues=20)
        
        # Calculate metrics
        metrics = calculate_metrics(results_df)
        
        # Save results
        save_results(results_df, metrics)
        
        print("\nExperiment completed successfully!")
        
    except Exception as e:
        print(f"Error running experiment: {e}")
        raise


if __name__ == "__main__":
    main()
