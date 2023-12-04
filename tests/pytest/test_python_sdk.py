
import os
import sys

# put plugin dir in path for importing
plugin_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, plugin_dir)

from autoload.databricks.python_sdk import execute_code
import pytest
from unittest.mock import MagicMock

class MockCommandExecution:
    def create(self, cluster_id, language) -> MagicMock:
        result = MagicMock()
        result.id = 'context_id'
        return result

    def execute(self, cluster_id, context_id, language, command):
        self.result = 'Mock command output'
        return self

    def destroy(self, cluster_id, context_id) -> None:
        pass

    def result(self):
        return self.result

class MockClient:
    def __init__(self, profile) -> None:
        self.profile = profile
        self.command_execution = MockCommandExecution()
        pass

@pytest.fixture
def mock_client(monkeypatch):
    def mock_client_class(*args, **kwargs):
        return MockClient(*args, **kwargs)
    
    monkeypatch.setattr("autoload.databricks.python_sdk.WorkspaceClient", mock_client_class)

def test_execute_code(mock_client):
    code = 'print("hello")'
    profile = 'mock_profile'
    cluster_id = 'mock_cluster_id'

    output = execute_code(code, profile, cluster_id)

    assert output == 'Mock command output'

