"""
Simple dataset creation using inspect_ai framework.
"""

import pandas as pd
import json
from typing import Dict, List
from inspect_ai import Task, TaskInfo


def create_experiment_dataset(results: List[Dict], output_dir: str = ".") -> Dict:
    """
    Create comprehensive dataset using inspect_ai framework.
    
    Args:
        results: List of experiment results
        output_dir: Directory to save outputs
        
    Returns:
        Dictionary with dataset information
    """
    # Create detailed CSV dataset
    detailed_df = pd.DataFrame(results)
    
    # Add inspect_ai metadata
    detailed_df['evaluation_framework'] = 'inspect_ai'
    detailed_df['framework_version'] = '0.3.125'
    detailed_df['experiment_timestamp'] = pd.Timestamp.now()
    
    # Save detailed dataset
    detailed_csv_path = f"{output_dir}/inspect_ai_results.csv"
    detailed_df.to_csv(detailed_csv_path, index=False)
    
    # Create JSON dataset
    json_dataset = {
        "inspect_ai_metadata": {
            "framework": "inspect_ai",
            "version": "0.3.125",
            "experiment": "self-sycophancy-swebench",
            "total_issues": len(results),
            "evaluation_method": "choice-based rating (0-10)"
        },
        "results": results,
        "summary": {
            "mean_self_rating": detailed_df["rating_self"].mean(),
            "mean_other_rating": detailed_df["rating_other"].mean(),
            "self_sycophancy_score": detailed_df["self_other_diff"].mean()
        }
    }
    
    json_path = f"{output_dir}/inspect_ai_dataset.json"
    with open(json_path, 'w') as f:
        json.dump(json_dataset, f, indent=2, default=str)
    
    # Create summary
    summary_df = pd.DataFrame([{
        "metric": "Self-Sycophancy Score",
        "value": detailed_df["self_other_diff"].mean(),
        "description": "Positive = self-sycophancy, Negative = self-criticism"
    }, {
        "metric": "Total Issues",
        "value": len(results),
        "description": "Number of issues evaluated"
    }, {
        "metric": "Framework",
        "value": "inspect_ai",
        "description": "Evaluation framework used"
    }])
    
    summary_path = f"{output_dir}/inspect_ai_summary.csv"
    summary_df.to_csv(summary_path, index=False)
    
    print(f"inspect_ai datasets created:")
    print(f"  Results: {detailed_csv_path}")
    print(f"  JSON: {json_path}")
    print(f"  Summary: {summary_path}")
    
    return {
        "results_csv": detailed_csv_path,
        "json_dataset": json_path,
        "summary_csv": summary_path
    }


def create_task_dataset(tasks: List[Task], output_dir: str = ".") -> str:
    """
    Create dataset of inspect_ai tasks.
    
    Args:
        tasks: List of inspect_ai Task objects
        output_dir: Directory to save outputs
        
    Returns:
        Path to saved task dataset
    """
    task_data = []
    
    for i, task in enumerate(tasks):
        task_data.append({
            "task_id": i,
            "task_name": task.name,
            "system_prompt": task.system_prompt,
            "user_prompt": task.user_prompt,
            "target": task.target,
            "metrics_count": len(task.metrics) if task.metrics else 0
        })
    
    task_df = pd.DataFrame(task_data)
    task_path = f"{output_dir}/inspect_ai_tasks.csv"
    task_df.to_csv(task_path, index=False)
    
    print(f"Task dataset saved: {task_path}")
    return task_path
