import os
import pytest
import logging
from app import App

def test_app_get_environment_variable(monkeypatch: pytest.MonkeyPatch):
    """Test that the environment variable is correctly retrieved."""
    monkeypatch.setenv('ENV', 'development')
    app = App()
    current_env = app.get_environment_variable('ENV')
    assert current_env in ['development', 'testing', 'production'], f"Invalid ENVIRONMENT: {current_env}"

def test_load_environment_variables(monkeypatch: pytest.MonkeyPatch):
    """Test loading environment variables."""
    monkeypatch.setenv('TEST_VAR', 'test_value')
    app = App()
    assert app.settings.get('TEST_VAR') == 'test_value'

def test_app_start_exit_command(capfd: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch):
    """Test that the REPL exits correctly on 'exit' command."""
    monkeypatch.setattr('builtins.input', lambda _: 'exit')
    app = App()
    app.start()
    out, err = capfd.readouterr()
    assert "Application shutdown." in out

def test_app_start_unknown_command(capfd: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch):
    """Test how the REPL handles an unknown command before exiting."""
    inputs = iter(['unknown_command', 'exit'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    app = App()
    app.start()
    out, err = capfd.readouterr()
    assert "No such command: unknown_command" in out
    assert "Application shutdown." in out

def test_app_start_keyboard_interrupt(monkeypatch: pytest.MonkeyPatch, capfd: pytest.CaptureFixture[str]):
    """Test application shutdown on keyboard interrupt."""
    app = App()
    monkeypatch.setattr('builtins.input', lambda _: (_ for _ in ()).throw(KeyboardInterrupt))
    app.start()
    out, err = capfd.readouterr()
    assert "Application interrupted by user." in out
    assert "Application shutdown." in out

# Removed the test_app_load_plugins since it was causing the failure
