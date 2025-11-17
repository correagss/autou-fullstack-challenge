import pytest

@pytest.fixture(autouse=True)
def mocked_environment_vars(monkeypatch):
    env_vars = {
        "OPENAI_API_KEY"    : 'key'
    }
    for key, value in env_vars.items():
        monkeypatch.setenv(key, value)