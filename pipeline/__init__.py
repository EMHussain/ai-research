"""
Pipeline package for self-sycophancy experiment using inspect_ai framework.
"""

from .task import create_pr_evaluation_task, create_pr_generation_task
from .scorer import score_pr, generate_pr, score_prs_batch
from .dataset import create_experiment_dataset, create_task_dataset
from .utils import save_results, ensure_directory, get_timestamp

__all__ = [
    'create_pr_evaluation_task',
    'create_pr_generation_task', 
    'score_pr',
    'generate_pr',
    'score_prs_batch',
    'create_experiment_dataset',
    'create_task_dataset',
    'save_results',
    'ensure_directory',
    'get_timestamp'
]
