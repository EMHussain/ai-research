"""
Simple experiment runner using inspect_ai pipeline.
"""

import random
import pandas as pd
from typing import List, Dict
from .scorer import score_pr, generate_pr, score_prs_batch
from .dataset import create_experiment_dataset
from concurrent.futures import ThreadPoolExecutor


def load_issues(n: int = 20) -> List[Dict]:
    """
    Load sample SWE-bench issues.
    
    Args:
        n: Number of issues to load (default: 20)
    
    Returns:
        List of issue dictionaries with sample data
    """
    # Sample issues for demonstration
    sample_issues = [
        {
            "id": f"issue_{i}",
            "title": f"Fix bug in function {i}",
            "description": f"This is a sample issue description for issue {i}. It describes a bug that needs fixing.",
            "repo": f"sample-repo-{i}",
            "base_commit": f"commit_hash_{i}"
        }
        for i in range(1, n + 1)
    ]
    
    return sample_issues


def run_sequential_experiment(n_issues: int = 20) -> pd.DataFrame:
    """
    Run experiment sequentially.
    
    Args:
        n_issues: Number of issues to process
        
    Returns:
        DataFrame with results
    """
    print(f"Loading {n_issues} issues...")
    issues = load_issues(n_issues)
    
    results = []
    
    for i, issue in enumerate(issues, 1):
        print(f"Processing issue {i}/{n_issues}: {issue['title']}")
        
        # Generate PR using inspect_ai
        pr = generate_pr(issue)
        
        # Score using inspect_ai
        rating_self = score_pr(pr, framing="self")
        rating_other = score_pr(pr, framing="other")
        
        # Ground truth
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
        
        print(f"  Issue {i} completed - Self: {rating_self}, Other: {rating_other}")
    
    return pd.DataFrame(results)


def run_parallel_experiment(n_issues: int = 20, max_workers: int = 5) -> pd.DataFrame:
    """
    Run experiment with parallel processing.
    
    Args:
        n_issues: Number of issues to process
        max_workers: Maximum parallel workers
        
    Returns:
        DataFrame with results
    """
    print(f"Loading {n_issues} issues for parallel processing...")
    issues = load_issues(n_issues)
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Generate all PRs in parallel
        pr_futures = {
            executor.submit(generate_pr, issue): issue 
            for issue in issues
        }
        
        prs = []
        for future in pr_futures:
            try:
                pr = future.result()
                prs.append(pr)
            except Exception as e:
                print(f"Error generating PR: {e}")
                prs.append({"title": "Error", "body": "Error", "diff": "Error"})
        
        # Score all PRs in parallel using inspect_ai
        print("Rating PRs using inspect_ai framework...")
        self_ratings = score_prs_batch(prs, "self")
        other_ratings = score_prs_batch(prs, "other")
        
        # Compile results
        results = []
        for i, (issue, pr, self_rating, other_rating) in enumerate(zip(issues, prs, self_ratings, other_ratings), 1):
            ground_truth = random.choice([0, 1])
            results.append({
                "issue_id": issue["id"],
                "issue_title": issue["title"],
                "pr_title": pr["title"],
                "rating_self": self_rating,
                "rating_other": other_rating,
                "ground_truth": ground_truth,
                "self_other_diff": self_rating - other_rating
            })
            print(f"  Issue {i} completed - Self: {self_rating}, Other: {other_rating}")
    
    return pd.DataFrame(results)


def calculate_metrics(df: pd.DataFrame) -> Dict:
    """
    Calculate experiment metrics.
    
    Args:
        df: DataFrame with results
        
    Returns:
        Dictionary with metrics
    """
    return {
        "mean_self": df["rating_self"].mean(),
        "mean_other": df["rating_other"].mean(),
        "mean_self_other_diff": df["self_other_diff"].mean(),
        "correlation_self_ground_truth": df["rating_self"].corr(df["ground_truth"]),
        "correlation_other_ground_truth": df["rating_other"].corr(df["ground_truth"]),
        "total_issues": len(df)
    }
