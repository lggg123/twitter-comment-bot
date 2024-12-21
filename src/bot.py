from tweepy import Client, API, OAuth1UserHandler
import logging
import time

class TwitterBot:
    def __init__(self, api_key, api_secret_key, access_token, access_token_secret, bearer_token=None):
        """Initialize Twitter bot with API credentials"""
        # Initialize v2 client with both OAuth 1.0a and Bearer token
        self.client = Client(
            consumer_key=api_key,
            consumer_secret=api_secret_key,
            access_token=access_token,
            access_token_secret=access_token_secret,
            bearer_token=bearer_token,
            wait_on_rate_limit=True  # This is already set, which is good
        )
        
        self.logger = logging.getLogger(__name__)
        self.logger.info("Successfully authenticated with Twitter API")

    def reply_to_tweets(self, search_terms, reply_text, max_tweets=10, retry_delay=60):
        """Search for tweets and reply to them using Twitter API v2"""
        self.logger.info(f"Starting to search for tweets with terms: {search_terms}")
        
        for term in search_terms:
            self.logger.info(f"Searching for term: {term}")
            while True:
                try:
                    # Ensure max_tweets is between 10 and 100
                    max_results = max(min(max_tweets, 100), 10)
                    
                    # Search tweets using v2 endpoint
                    tweets = self.client.search_recent_tweets(
                        query=term,
                        max_results=max_results,
                        tweet_fields=['author_id', 'conversation_id', 'created_at'],
                        expansions=['author_id']
                    )
                    
                    if tweets.data:
                        for tweet in tweets.data:
                            try:
                                # Add delay between replies to avoid rate limits
                                time.sleep(retry_delay)
                                
                                # Reply to tweet
                                response = self.client.create_tweet(
                                    text=reply_text,
                                    in_reply_to_tweet_id=tweet.id
                                )
                                self.logger.info(f"Replied to tweet {tweet.id}")
                            except Exception as e:
                                self.logger.error(f"Error replying to tweet {tweet.id}: {str(e)}")
                                if "Rate limit" in str(e):
                                    self.logger.info(f"Rate limit hit. Waiting {retry_delay} seconds...")
                                    time.sleep(retry_delay)
                                    continue
                    else:
                        self.logger.info(f"No tweets found for term: {term}")
                    
                    # If we get here, we've successfully processed all tweets
                    break
                        
                except Exception as e:
                    self.logger.error(f"Error in reply_to_tweets: {str(e)}")
                    if "Rate limit" in str(e):
                        self.logger.info(f"Rate limit hit. Waiting {retry_delay} seconds...")
                        time.sleep(retry_delay)
                        continue
                    raise e
    
    
