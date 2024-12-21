from src.bot import TwitterBot
from src.config import Config
from src.utils.logger import setup_logger

def main():
    logger = setup_logger()
    config = Config()
    bot = TwitterBot(
        config.secrets['twitter']['api_key'],
        config.secrets['twitter']['api_secret_key'],
        config.secrets['twitter']['access_token'],
        config.secrets['twitter']['access_token_secret']
    )
    bot.run()

if __name__ == "__main__":
    main()