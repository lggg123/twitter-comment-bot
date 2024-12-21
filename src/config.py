import yaml
import os

class Config:
    def __init__(self, config_path: str = None, secrets_path: str = None):
        """Initialize config from YAML files"""
        print(f"Current working directory: {os.getcwd()}")
        print(f"Config path received: {config_path}")
        print(f"Secrets path received: {secrets_path}")
        
        self.config = self._load_config(config_path) if config_path else {}
        self.secrets = self._load_secrets(secrets_path) if secrets_path else {}
        
        # Set Twitter credentials from secrets.yaml
        if 'twitter' in self.secrets:
            self.twitter_api_key = self.secrets['twitter']['api_key']
            self.twitter_api_secret = self.secrets['twitter']['api_secret_key']
            self.twitter_access_token = self.secrets['twitter']['access_token']
            self.twitter_access_token_secret = self.secrets['twitter']['access_token_secret']
            self.twitter_bearer_token = self.secrets['twitter'].get('bearer_token')
        else:
            raise ValueError("Twitter credentials not found in secrets.yaml")

    def _load_config(self, path: str) -> dict:
        print(f"Attempting to load config from: {path}")
        print(f"File exists: {os.path.exists(path)}")
        with open(path, 'r') as file:
            return yaml.safe_load(file)

    def _load_secrets(self, path: str) -> dict:
        print(f"Attempting to load secrets from: {path}")
        print(f"File exists: {os.path.exists(path)}")
        with open(path, 'r') as file:
            return yaml.safe_load(file)


def load_config() -> Config:
    """Helper function to create a Config instance from YAML files"""
    # Get the current working directory
    current_dir = os.getcwd()
    print(f"Current working directory: {current_dir}")
    
    # Look for config files in the current directory first
    config_path = os.path.join(current_dir, "config.yaml")
    secrets_path = os.path.join(current_dir, "secrets.yaml")
    
    # If not found, try the config subdirectory
    if not os.path.exists(config_path):
        config_path = os.path.join(current_dir, "config", "config.yaml")
        secrets_path = os.path.join(current_dir, "config", "secrets.yaml")
    
    print(f"Looking for config file at: {config_path}")
    print(f"Looking for secrets file at: {secrets_path}")
    print(f"Config file exists: {os.path.exists(config_path)}")
    print(f"Secrets file exists: {os.path.exists(secrets_path)}")
    
    return Config(
        config_path=config_path,
        secrets_path=secrets_path
    )
