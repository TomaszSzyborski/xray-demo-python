import json
from typing import Dict, List

class BehaveParser:
    def parse(self, behave_json_path: str) -> Dict:
        """Parse Behave JSON output and return test results in Xray format."""
        with open(behave_json_path, 'r') as f:
            behave_data = json.load(f)
            
        test_results = []
        
        for feature in behave_data:
            for scenario in feature['elements']:
                if scenario['type'] == 'scenario':
                    result = {
                        'testKey': f"{feature['name']}.{scenario['name']}",
                        'start': None,  # Will be set during execution
                        'finish': None,  # Will be set during execution
                        'comment': '',
                        'status': 'PASSED'
                    }
                    
                    # Check steps for failures
                    for step in scenario['steps']:
                        if step['result']['status'] == 'failed':
                            result['status'] = 'FAILED'
                            result['comment'] = step['result'].get('error_message', '')
                            break
                        elif step['result']['status'] == 'skipped':
                            result['status'] = 'SKIPPED'
                            
                    test_results.append(result)
                    
        return {
            'testExecutionKey': None,  # Will be set during execution
            'tests': test_results
        }