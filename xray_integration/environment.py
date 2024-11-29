from behave.model import Scenario, Step
from behave.runner import Context
from .config import XrayConfig
from .behave_hooks import XrayBehaveReporter

def before_all(context: Context):
    """Initialize XrayBehaveReporter before all tests."""
    config = XrayConfig(
        jira_base_url=context.config.userdata.get('jira_base_url'),
        xray_base_url=context.config.userdata.get('xray_base_url'),
        personal_access_token=context.config.userdata.get('xray_token'),
        project_key=context.config.userdata.get('project_key'),
        test_plan_key=context.config.userdata.get('test_plan_key')
    )
    reporter = XrayBehaveReporter(config)
    reporter.before_all(context)

def before_scenario(context: Context, scenario: Scenario):
    """Report scenario start to Xray."""
    context.xray_reporter.before_scenario(context, scenario)

def after_step(context: Context, step: Step):
    """Report step completion to Xray."""
    context.xray_reporter.after_step(context, step)

def after_scenario(context: Context, scenario: Scenario):
    """Report scenario completion to Xray."""
    context.xray_reporter.after_scenario(context, scenario)