from xray_integration import XrayConfig, XrayClient, JUnitParser, BehaveParser

def main():
    # Configure Xray connection
    config = XrayConfig(
        jira_base_url="https://your-jira-instance.com",
        xray_base_url="https://your-xray-instance.com",
        personal_access_token="your-pat-token",
        project_key="PROJECT",
        test_plan_key="TEST-1"  # Optional
    )
    
    # Initialize Xray client
    client = XrayClient(config)
    
    # Example with JUnit results
    junit_parser = JUnitParser()
    junit_results = junit_parser.parse("path/to/junit-results.xml")
    client.upload_test_results(junit_results)
    
    # Example with Behave results
    behave_parser = BehaveParser()
    behave_results = behave_parser.parse("path/to/behave-results.json")
    client.upload_test_results(behave_results)

if __name__ == "__main__":
    main()