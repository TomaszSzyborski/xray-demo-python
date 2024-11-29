from typing import Dict, List
import xml.etree.ElementTree as ET

class JUnitParser:
    def parse(self, junit_file_path: str) -> Dict:
        """Parse JUnit XML file and return test results in Xray format."""
        tree = ET.parse(junit_file_path)
        root = tree.getroot()
        
        test_results = []
        
        for test_suite in root.findall('.//testcase'):
            result = {
                'testKey': test_suite.get('classname') + '.' + test_suite.get('name'),
                'start': None,  # Will be set during execution
                'finish': None,  # Will be set during execution
                'comment': '',
                'status': 'PASSED'
            }
            
            failure = test_suite.find('failure')
            error = test_suite.find('error')
            skipped = test_suite.find('skipped')
            
            if failure is not None:
                result['status'] = 'FAILED'
                result['comment'] = failure.get('message', '')
            elif error is not None:
                result['status'] = 'FAILED'
                result['comment'] = error.get('message', '')
            elif skipped is not None:
                result['status'] = 'SKIPPED'
                result['comment'] = skipped.get('message', '')
                
            test_results.append(result)
            
        return {
            'testExecutionKey': None,  # Will be set during execution
            'tests': test_results
        }