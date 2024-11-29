# Xray Test Results Integration

This Python package provides integration between test results (JUnit XML or Behave JSON) and Jira Xray (on-premises).

## Features

- Support for JUnit XML test results
- Support for Behave JSON test results
- Real-time test execution updates with Behave hooks
- Automatic test execution creation
- Optional test plan integration
- Personal Access Token authentication

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### 1. Configure your Xray connection:

```python
from xray_integration import XrayConfig, XrayClient

config = XrayConfig(
    jira_base_url="https://your-jira-instance.com",
    xray_base_url="https://your-xray-instance.com",
    personal_access_token="your-pat-token",
    project_key="PROJECT",
    test_plan_key="TEST-1"  # Optional
)
```

### 2. Upload JUnit results:

```python
from xray_integration import JUnitParser

junit_parser = JUnitParser()
client = XrayClient(config)

results = junit_parser.parse("path/to/junit-results.xml")
client.upload_test_results(results)
```

### 3. Upload Behave results:

```python
from xray_integration import BehaveParser

behave_parser = BehaveParser()
client = XrayClient(config)

results = behave_parser.parse("path/to/behave-results.json")
client.upload_test_results(results)
```

### 4. Real-time Behave Integration:

1. Create a `behave.ini` file with your Xray configuration:
```ini
[behave.userdata]
jira_base_url = https://your-jira-instance.com
xray_base_url = https://your-xray-instance.com
xray_token = your-pat-token
project_key = PROJECT
test_plan_key = TEST-1
```

2. Copy the `environment.py` file to your Behave features directory.

3. Run your Behave tests normally:
```bash
behave
```

Tests will now update in Xray in real-time as they execute!

## Configuration Options

- `jira_base_url`: Base URL of your Jira instance
- `xray_base_url`: Base URL of your Xray instance
- `personal_access_token`: Your Xray Personal Access Token
- `project_key`: Jira project key
- `test_plan_key`: (Optional) Key of the test plan to associate results with
- `test_execution_key`: (Optional) Key of an existing test execution to update

## Error Handling

The client will raise exceptions for:
- Invalid authentication
- Network errors
- Invalid test results format
- Missing required fields

## Best Practices

1. Store configuration securely (e.g., environment variables or behave.ini)
2. Handle exceptions appropriately in your implementation
3. Use meaningful test execution names
4. Regularly clean up old test executions
5. Monitor real-time test execution updates for early feedback