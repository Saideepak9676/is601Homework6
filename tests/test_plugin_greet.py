import pytest
from app import App

def test_app_greet_command(capfd, monkeypatch):
    """Test that the REPL correctly handles the 'greet' command and outputs 'Hello, World!'."""
    # Simulate REPL input sequence: 'greet' followed by 'exit'
    inputs = iter(['greet', 'exit'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    app = App()

    # Start the app, expect it to exit without raising an error
    app.start()

    # Capture output from the 'greet' command
    out, err = capfd.readouterr()

    # Verify 'Hello, World!' was printed to stdout
    assert "Hello, World!" in out, "The 'greet' command did not produce the expected output."