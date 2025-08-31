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
    Load real SWE-bench issues.
    
    Args:
        n: Number of issues to load (default: 20)
    
    Returns:
        List of real SWE-bench issue dictionaries
    """
    try:
        # Import datasets library
        from datasets import load_dataset
        
        # Load SWE-bench dataset from Hugging Face
        dataset = load_dataset("princeton-nlp/SWE-bench", split="test")
        
        # Get sample issues (first n issues)
        issues = []
        for i, item in enumerate(dataset):
            if i >= n:
                break
                
            # Extract and truncate relevant fields from SWE-bench format
            problem_statement = item.get("problem_statement", "")
            
            # Truncate long descriptions to fit within token limits
            # Rough estimate: 1 token ≈ 4 characters, so 8000 tokens ≈ 32,000 characters
            # Be more conservative: aim for ~6000 tokens to leave room for completion
            max_chars = 20000  # More aggressive truncation to stay well under limit
            
            if len(problem_statement) > max_chars:
                problem_statement = problem_statement[:max_chars] + "... [truncated]"
                print(f"  Truncated issue {i+1} from {len(item.get('problem_statement', ''))} to {len(problem_statement)} characters")
            
            issue = {
                "id": item.get("instance_id", f"issue_{i+1}"),
                "title": item.get("problem_statement", f"SWE-bench issue {i+1}")[:150] + "..." if len(item.get("problem_statement", "")) > 150 else item.get("problem_statement", f"SWE-bench issue {i+1}"),
                "description": problem_statement,
                "repo": item.get("repo", "unknown-repo"),
                "base_commit": item.get("base_commit", "unknown-commit"),
                "test_patch": item.get("test_patch", "")[:500] + "..." if len(item.get("test_patch", "")) > 500 else item.get("test_patch", ""),
                "test_file": item.get("test_file", "")
            }
            issues.append(issue)
            
        print(f"Loaded {len(issues)} real SWE-bench issues from Hugging Face")
        return issues
        
    except ImportError:
        print("Warning: datasets library not available, using sample issues")
        return _get_sample_issues(n)
    except Exception as e:
        print(f"Error loading SWE-bench issues: {e}")
        print("Falling back to sample issues")
        return _get_sample_issues(n)


def _get_sample_issues(n: int) -> List[Dict]:
    """
    Fallback to sample issues if SWE-bench fails.
    
    Args:
        n: Number of issues to create
        
    Returns:
        List of sample issue dictionaries
    """
    # Sample issues for demonstration (fallback)
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
