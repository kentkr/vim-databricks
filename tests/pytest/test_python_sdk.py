
import os
import sys
# put plugin dir in path for importing
plugin_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, plugin_dir)
from unittest.mock import MagicMock
from autoload.databricks.python_sdk import context_is_running
import pytest

@pytest.fixture(scope='class')
def mock_client(monkeypatch):
    mock_client=MagicMock()
    monkeypatch.setattr('autoload.databricks.python_sdk.WorkspaceClient', mock_client)
    yield mock_client

# context_is_running
class TestContext:
    @classmethod
    def setup_class(cls, mock_client):
        cls.mock_client = mock_client 

    def update_context_status_value(self, value):
        self.mock_client().command_execution.context_status().status.value=value


    def test_context_running(self):
        self.update_context_status_value('Running')
        assert context_is_running('','','')


    def test_context_not_running(self):
        self.update_context_status_value('Not correct value')
        assert not context_is_running('','','')

    
    def test_context_exception(self):
        self.update_context_status_value(Exception)
        assert not context_is_running('','','')

