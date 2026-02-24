import unittest
from unittest.mock import patch
import os
import sys

# Add scripts directory to path so we can import action_entrypoint
sys.path.append(os.path.join(os.path.dirname(__file__), '../scripts'))
from action_entrypoint import get_env_var

class TestGetEnvVar(unittest.TestCase):
    @patch.dict(os.environ, {"INPUT_MY_VAR": "input_value", "MY_VAR": "env_value"})
    def test_get_env_var_prioritizes_input(self):
        # The function converts name to uppercase and prepends INPUT_
        self.assertEqual(get_env_var("my_var"), "input_value")

    @patch.dict(os.environ, {"MY_VAR": "env_value"}, clear=True)
    def test_get_env_var_uses_env_if_no_input(self):
        # If INPUT_MY_VAR is not set, it should check MY_VAR
        self.assertEqual(get_env_var("MY_VAR"), "env_value")

    @patch.dict(os.environ, {}, clear=True)
    def test_get_env_var_uses_default_if_none_set(self):
        # If neither is set, return default
        self.assertEqual(get_env_var("MY_VAR", "default_value"), "default_value")

    @patch.dict(os.environ, {}, clear=True)
    def test_get_env_var_returns_none_if_no_default(self):
        # Default is None
        self.assertIsNone(get_env_var("MY_VAR"))

    @patch.dict(os.environ, {"INPUT_MY_VAR": ""}, clear=True)
    def test_get_env_var_handles_empty_string_input(self):
        # Empty string should be returned if set
        self.assertEqual(get_env_var("my_var"), "")

if __name__ == '__main__':
    unittest.main()
