from dataclasses import dataclass
from typing import Optional

@dataclass
class XrayConfig:
    jira_base_url: str
    xray_base_url: str
    personal_access_token: str
    project_key: str
    test_plan_key: Optional[str] = None
    test_execution_key: Optional[str] = None