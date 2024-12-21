import pytest
import os
import yaml
from src.config import Config

@pytest.fixture
def sample_config_file(tmp_path):
    config_data = {
        'bot': {
            'search_terms': ["#python", "#coding"],
            'reply_text': "Hello! I'm a bot. How can I help you today?",
            'ma_tweets': 10,
            'sleep_time': 3600
        }
    }
    config_file = tmp_path / "config.yaml"
    with open(config_file, "w") as f:
        yaml.dump(config_data, f)
    return config_file

@pytest.fixture
def sample_secrets_file(tmp_path):
    secrets_data = {
        'twitter': {
            'api_key': 'test_api_key',
            'api_secret_key': 'test_api_secret_key',
            'access_token': 'test_access_token',
            'access_token_secret': 'test_access_token_secret'
        }
    }
    secrets_file = tmp_path / "secrets.yaml"
    with open(secrets_file, "w") as f:
        yaml.dump(secrets_data, f)
    return secrets_file

def test_config_loading(sample_config_file, sample_secrets_file):
    config = Config(str(sample_config_file), str(sample_secrets_file))

    assert config.config['bot']['search_terms'] == ["#python", "#coding"]
    assert config.config['bot']['ma_tweets'] == 10
    assert config.secrets['twitter']['api_key'] == 'test_api_key'

def test_config_file_not_found():
    with pytest.raises(FileNotFoundError):
        Config("nonexistent_config.yaml", "nonexistent_secrets.yaml")