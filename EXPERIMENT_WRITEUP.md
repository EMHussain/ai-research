# Self-Sycophancy Experiment: What We Built

## **What We Built**

We created a Python experiment to test if AI language models show self-sycophancy bias. The system works like this:

1. **Generate Fake Issues**: We create 10 made-up software bug reports (like "Fix the login button" or "Fix the search function")

2. **AI Creates Solutions**: We ask an AI model to write pull requests (code changes) for each issue

3. **AI Rates Its Own Work**: We ask the same AI to rate how good its own solution is (0-10 scale)

4. **AI Rates Other Work**: We ask the AI to rate a different solution for the same issue

5. **Compare the Ratings**: We see if the AI gives itself higher scores than others

## **How It Works**

The experiment uses the OpenRouter API to call AI models and the inspect_ai framework for evaluation. We run everything sequentially (one at a time) to avoid hitting API rate limits. All results get saved into a `results` folder with CSV files, JSON data, and visualizations.

## **What We Found**

Our test showed the AI model was actually slightly self-critical (-0.1 difference), meaning it rated its own work a bit lower than others' work. This suggests the model doesn't have strong self-sycophancy bias, which is good for fairness in AI evaluation systems.

The experiment successfully demonstrates how to measure and analyze self-sycophancy in AI models using industry-standard tools and frameworks.
