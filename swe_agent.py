from typing import Dict, List
import llm_client


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


def run_agent(issue: Dict) -> Dict:
    """
    Simulate PR creation for a given issue.
    
    Args:
        issue: Issue dictionary with title and description
    
    Returns:
        PR dictionary with title, body, and diff
    """
    prompt = f"""
    Issue: {issue['title']}
    Description: {issue['description']}
    
    Please propose a solution for this issue. Return your response in the following format:
    - Title: [PR title]
    - Body: [PR description]
    - Diff: [code changes in diff format]
    """
    
    try:
        response = llm_client.call_model(prompt)
        
        # Parse response to extract components
        lines = response.split('\n')
        title = ""
        body = ""
        diff = ""
        
        for line in lines:
            if line.startswith('- Title:'):
                title = line.replace('- Title:', '').strip()
            elif line.startswith('- Body:'):
                body = line.replace('- Body:', '').strip()
            elif line.startswith('- Diff:'):
                diff = line.replace('- Diff:', '').strip()
        
        # Fallback if parsing fails
        if not title:
            title = f"Fix: {issue['title']}"
        if not body:
            body = f"Addresses issue: {issue['description']}"
        if not diff:
            diff = f"# Sample diff for {issue['title']}\n+ # TODO: Implement actual fix"
        
        return {
            "issue_id": issue["id"],
            "title": title,
            "body": body,
            "diff": diff,
            "raw_response": response
        }
        
    except Exception as e:
        # Fallback if LLM call fails
        return {
            "issue_id": issue["id"],
            "title": f"Fix: {issue['title']}",
            "body": f"Addresses issue: {issue['description']}",
            "diff": f"# Sample diff for {issue['title']}\n+ # TODO: Implement actual fix",
            "raw_response": f"Error: {str(e)}"
        }
