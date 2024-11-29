import requests
from datetime import datetime
from typing import Dict
from .config import XrayConfig

class XrayClient:
    def __init__(self, config: XrayConfig):
        self.config = config
        self.headers = {
            'Authorization': f'Bearer {config.personal_access_token}',
            'Content-Type': 'application/json'
        }
        
    def create_test_execution(self, summary: str) -> str:
        """Create a new test execution in Xray and return its key."""
        url = f"{self.config.xray_base_url}/api/v2/testExecution"
        
        payload = {
            'fields': {
                'project': {'key': self.config.project_key},
                'summary': summary,
                'issuetype': {'name': 'Test Execution'}
            }
        }
        
        response = requests.post(url, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()['key']
        
    def upload_test_results(self, test_results: Dict) -> Dict:
        """Upload test results to Xray."""
        url = f"{self.config.xray_base_url}/api/v2/testExecutions"
        
        # Add execution information
        if not test_results['testExecutionKey']:
            if self.config.test_execution_key:
                test_results['testExecutionKey'] = self.config.test_execution_key
            else:
                # Create new test execution if none specified
                summary = f"Test Execution {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                test_results['testExecutionKey'] = self.create_test_execution(summary)
        
        # Add test plan if specified
        if self.config.test_plan_key:
            test_results['testPlanKey'] = self.config.test_plan_key
            
        response = requests.post(url, headers=self.headers, json=test_results)
        response.raise_for_status()
        return response.json()