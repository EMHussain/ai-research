"""
Utility functions for the inspect_ai pipeline.
"""

import os
import matplotlib.pyplot as plt
import pandas as pd
from typing import Dict


def save_results(df: pd.DataFrame, metrics: Dict, output_dir: str = "results"):
    """
    Save results and create visualization.
    
    Args:
        df: DataFrame with experiment results
        metrics: Dictionary with calculated metrics
        output_dir: Directory to save outputs (default: results)
    """
    # Ensure results directory exists
    os.makedirs(output_dir, exist_ok=True)
    
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


def ensure_directory(path: str):
    """
    Ensure a directory exists, create if it doesn't.
    
    Args:
        path: Directory path to ensure exists
    """
    os.makedirs(path, exist_ok=True)


def get_timestamp():
    """
    Get current timestamp for file naming.
    
    Returns:
        Formatted timestamp string
    """
    from datetime import datetime
    return datetime.now().strftime("%Y%m%d_%H%M%S")
