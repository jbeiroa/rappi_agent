import pytest
from src.agents.analyst.tools import run_pandas_query
from unittest.mock import patch, MagicMock
import pandas as pd

def test_run_pandas_query_valid(mock_excel_file):
    """Test a valid pandas query string."""
    with patch('pathlib.Path.exists', return_value=True):
        # Result of Sum(Orders) = 100+110+...+180 = 1260
        result = run_pandas_query("df[df['METRIC'] == 'Orders']['VALUE'].sum()")
        assert '1260' in str(result)

def test_run_pandas_query_security_eval(mock_excel_file):
    """Verify security: attempt malicious injection."""
    with patch('pathlib.Path.exists', return_value=True):
        # Malicious code trying to access os.system via __builtins__ (which should be restricted)
        # Note: In our implementation, we set __builtins__ to empty dict.
        bad_code = "__import__('os').system('echo pwned')"
        result = run_pandas_query(bad_code)
        
        # Should return an error string rather than executing
        assert "Error" in result
        # Check specific restricted error (name __import__ not defined)
        assert "__import__" in result or "not defined" in result

def test_run_pandas_query_syntax_error(mock_excel_file):
    """Test invalid python code."""
    with patch('pathlib.Path.exists', return_value=True):
        result = run_pandas_query("df[.query(]")
        assert "Error" in result
        # Check that it captured some kind of syntax/parenthesis error
        assert any(keyword in result.lower() for keyword in ["invalid syntax", "parenthesis", "match"])
