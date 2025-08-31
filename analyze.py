"""
Main experiment runner using inspect_ai pipeline.
"""

import matplotlib.pyplot as plt
from pipeline.experiment import run_sequential_experiment, run_parallel_experiment, calculate_metrics
from pipeline.dataset import create_experiment_dataset
from pipeline.utils import save_results


def main():
    """Main function to run the experiment."""
    print("Starting self-sycophancy experiment with inspect_ai pipeline...")

    # Simple configuration
    USE_PARALLEL = True  # Set to False for sequential processing
    N_ISSUES = 20  # Increased to 20 for more comprehensive results
    MAX_PARALLEL_WORKERS = 1  # Single worker to avoid rate limiting
    RESULTS_DIR = "results"  # All outputs go to results folder

    try:
        if USE_PARALLEL:
            print(f"Running parallel experiment with {N_ISSUES} issues (max {MAX_PARALLEL_WORKERS} workers)...")
            results_df = run_parallel_experiment(n_issues=N_ISSUES, max_workers=MAX_PARALLEL_WORKERS)
        else:
            print(f"Running sequential experiment with {N_ISSUES} issues...")
            results_df = run_sequential_experiment(n_issues=N_ISSUES)

        # Calculate metrics
        metrics = calculate_metrics(results_df)

        # Save basic results to results folder
        save_results(results_df, metrics, RESULTS_DIR)

        # Create comprehensive datasets using inspect_ai framework
        print("\nCreating comprehensive datasets...")
        dataset_info = create_experiment_dataset(results_df.to_dict('records'), RESULTS_DIR)

        print("\nExperiment completed successfully!")
        if USE_PARALLEL:
            print(f"Parallel processing completed with {MAX_PARALLEL_WORKERS} workers")
        else:
            print(f"Sequential processing completed")
        print(f"Datasets available: {len(dataset_info)} formats")
        print(f"All results saved to: {RESULTS_DIR}/ folder")

    except Exception as e:
        print(f"Error running experiment: {e}")
        raise


if __name__ == "__main__":
    main()
