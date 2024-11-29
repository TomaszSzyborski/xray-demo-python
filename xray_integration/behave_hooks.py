from datetime import datetime
from typing import Optional
from behave.model import Scenario, Step
from behave.runner import Context
from .xray_client import XrayClient
from .config import XrayConfig

class XrayBehaveReporter:
    def __init__(self, config: XrayConfig):
        self.client = XrayClient(config)
        self.test_execution_key: Optional[str] = None
        self.current_scenario: Optional[dict] = None
        
    def before_all(self, context: Context):
        """Create a new test execution before running any tests."""
        summary = f"Behave Test Execution {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        self.test_execution_key = self.client.create_test_execution(summary)
        context.xray_reporter = self
        
    def before_scenario(self, context: Context, scenario: Scenario):
        """Initialize scenario tracking before each scenario."""
        self.current_scenario = {
            'testKey': f"{scenario.feature.name}.{scenario.name}",
            'start': datetime.now().isoformat(),
            'status': 'EXECUTING',
            'comment': ''
        }
        self._update_current_test()
        
    def after_step(self, context: Context, step: Step):
        """Update scenario status after each step."""
        if step.status == 'failed':
            self.current_scenario['status'] = 'FAILED'
            self.current_scenario['comment'] = step.error_message
            self._update_current_test()
        elif step.status == 'skipped':
            if self.current_scenario['status'] != 'FAILED':
                self.current_scenario['status'] = 'SKIPPED'
                self._update_current_test()
                
    def after_scenario(self, context: Context, scenario: Scenario):
        """Finalize scenario status after completion."""
        self.current_scenario['finish'] = datetime.now().isoformat()
        if self.current_scenario['status'] == 'EXECUTING':
            self.current_scenario['status'] = 'PASSED'
        self._update_current_test()
        self.current_scenario = None
        
    def _update_current_test(self):
        """Send current test status to Xray."""
        if self.current_scenario and self.test_execution_key:
            payload = {
                'testExecutionKey': self.test_execution_key,
                'tests': [self.current_scenario]
            }
            self.client.upload_test_results(payload)