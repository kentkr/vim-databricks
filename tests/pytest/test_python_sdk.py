
import os
import sys
# put plugin dir in path for importing
plugin_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, plugin_dir)
from unittest.mock import MagicMock, patch
from autoload.databricks.python_sdk import context_is_running


def test_context_running():
    with patch('autoload.databricks.python_sdk.WorkspaceClient') as MockedClient:
        mock_command_execution=MagicMock()
        mock_command_execution.command_execution.context_status().status.value='Running'
        MockedClient.return_value=mock_command_execution
        assert context_is_running('','','')

def test_context_not_running():
    with patch('autoload.databricks.python_sdk.WorkspaceClient') as MockedClient:
        mock_command_execution=MagicMock()
        mock_command_execution.command_execution.context_status().status.value='Something else'
        MockedClient.return_value=mock_command_execution
        assert not context_is_running('','','')

def test_context_exception():
    with patch('autoload.databricks.python_sdk.WorkspaceClient') as MockedClient:
        mock_command_execution=MagicMock()
        mock_command_execution.command_execution.context_status().side_effect=Exception
        MockedClient.return_value=mock_command_execution
        assert not context_is_running('','','')


