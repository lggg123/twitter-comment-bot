from src.bot import TwitterBot
from src.config import load_config

def main():
    print("Starting bot...")
    
    try:
        # Load config
        print("Loading configuration...")
        config = load_config()
        print("Config loaded successfully")

        # Create bot instance
        print("Creating bot instance...")
        bot = TwitterBot(
            api_key=config.twitter_api_key,
            api_secret_key=config.twitter_api_secret,
            access_token=config.twitter_access_token,
            access_token_secret=config.twitter_access_token_secret,
            bearer_token=config.twitter_bearer_token
        )
        print("Bot instance created successfully")

        # Run bot
        print("Starting to search for tweets...")
        bot.reply_to_tweets(
            search_terms=['#python'], 
            reply_text="Awesome python all the way make some magic!",
            max_tweets=10,
            retry_delay=120
        )
        print("Bot finished running")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise

if __name__ == "__main__":
    print("Script started")
    main()
    print("Script finished")