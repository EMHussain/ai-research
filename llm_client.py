import os
import requests
from typing import Optional

# Try to load .env file if python-dotenv is available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


def call_model(prompt: str, model: str = "google/gemma-2-9b-it:free") -> str:
    """
    Call OpenRouter API to get model response.
    
    Args:
        prompt: Input text prompt
        model: Model identifier (default: google/gemma-2-9b-it:free)
    
    Returns:
        Model's text output
        
    Raises:
        ValueError: If API key not found
        requests.RequestException: If API call fails
    """
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY environment variable not set. Please set it in your environment or create a .env file.")
    
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:3000",  # Required by OpenRouter
        "X-Title": "Self-Sycophancy-Experiment"  # Optional but helpful
    }
    
    data = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 500,
        "temperature": 0.7
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        
        # Print response details for debugging
        if response.status_code != 200:
            print(f"API Error: {response.status_code}")
            print(f"Response: {response.text}")
            response.raise_for_status()
        
        response_data = response.json()
        
        # Check if response has the expected structure
        if "choices" not in response_data or not response_data["choices"]:
            raise ValueError(f"Unexpected API response format: {response_data}")
        
        return response_data["choices"][0]["message"]["content"]
        
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
        print(f"Response: {e.response.text if e.response else 'No response'}")
        raise
    except Exception as e:
        print(f"Error calling OpenRouter API: {e}")
        raise
