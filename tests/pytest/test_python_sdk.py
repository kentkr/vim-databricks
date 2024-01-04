
import os
import sys
# put plugin dir in path for importing
plugin_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, plugin_dir)
from unittest.mock import MagicMock
from autoload.databricks.python_sdk import context_is_running, get_execution_context
import pytest
import tempfile


class TestContextRunning:
    @pytest.fixture(autouse=True)
    def mock_client(self, monkeypatch):
        mock_client=MagicMock()
        monkeypatch.setattr('autoload.databricks.python_sdk.WorkspaceClient', mock_client)
        self.mock_client=mock_client
        yield mock_client


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

class TestGetContext:
    @pytest.fixture()
    def mock_client(self, monkeypatch):
        mock_client=MagicMock()
        mock_client().command_execution.create().result().id = 'new_string'
        monkeypatch.setattr('autoload.databricks.python_sdk.WorkspaceClient', mock_client)
        yield mock_client

    @pytest.fixture()
    def patch_shit(self, monkeypatch):
        def mock_exists():
            return True
        def mock_open():
            return 'this_id', '2023-12-29 11:34:20.988413'
        def mock_context_is_running():
            return True
        monkeypatch.setattr('os.path.exists', mock_exists)
        monkeypatch.setattr('builtins.open', mock_open)
        monkeypatch.setattr('autoload.databricks.python_sdk.context_is_running', mock_context_is_running)

    def test_get_context_from_file(self, patch_shit):
        assert get_execution_context('', '') == 'this_id'
    

    def test_get_context_from_client(self):
        assert get_execution_context('', '') == 'new_string'

