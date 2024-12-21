import pytest
from unittest.mock import Mock, patch
from src.bot import TwitterBot

@pytest.fixture
def mock_tweepy():
    with patch('tweepy.OAuth1UserHandler') as mock_auth, \
         patch('tweepy.API') as mock_api:
        # Configure the mock API
        api_instance = Mock()
        mock_api.return_value = api_instance
        
        # Set up the search_tweets mock to return a list
        mock_tweets = []
        api_instance.search_tweets.return_value = mock_tweets
        
        # Make the auth handler return itself after set_access_token
        mock_auth.return_value.set_access_token.return_value = None
        
        # Important: Make sure the API instance is used
        mock_api.return_value = api_instance
        
        yield {
            'auth': mock_auth,
            'api': mock_api,
            'api_instance': api_instance,
            'tweets': mock_tweets
        }

@pytest.fixture
def twitter_bot(mock_tweepy):
    with patch('tweepy.OAuth1UserHandler'), patch('tweepy.API') as mock_api:
        # Create the bot with the mocked API
        bot = TwitterBot(
            api_key='test_api_key',
            api_secret='test_api_secret',
            access_token='test_access_token',
            access_token_secret='test_access_token_secret'
        )
        # Explicitly set the API instance
        bot.api = mock_tweepy['api_instance']
        print(f"\nIn fixture - Bot API instance: {bot.api}")
        print(f"In fixture - Mock API instance: {mock_tweepy['api_instance']}")
        return bot

def test_bot_initialization(mock_tweepy):
    # Create bot with same credentials as in fixture
    bot = TwitterBot(
        api_key='test_api_key',
        api_secret='test_api_secret',
        access_token='test_access_token',
        access_token_secret='test_access_token_secret'
    )
    
    # Verify Twitter authentication was attempted with correct credentials
    mock_tweepy['auth'].assert_called_once_with('test_api_key', 'test_api_secret')
    mock_tweepy['api'].assert_called_once()

def test_reply_to_tweets(twitter_bot, mock_tweepy):
    # Create mock tweet
    mock_tweet = Mock()
    mock_tweet.configure_mock(
        id='123',
        user=Mock(screen_name='test_user'),
        retweeted_status=None,
        in_reply_to_status_id=None
    )
    
    # Create a new mock API instance specifically for this test
    mock_api = Mock()
    mock_api.search_tweets.return_value = [mock_tweet]
    
    # Replace the bot's API with our mock
    twitter_bot.api = mock_api
    
    # Mock time.sleep to prevent waiting
    with patch('time.sleep'):
        # Run the method
        twitter_bot.reply_to_tweets(
            search_terms=['#test'],
            reply_text='Text reply',
            max_tweets=1
        )
    
    # Verify tweet reply was attempted
    mock_api.update_status.assert_called_once_with(
        status='@test_user Text reply',
        in_reply_to_status_id='123'
    )

def test_skip_retweets_and_replies(twitter_bot, mock_tweepy):
    # Create mock retweet and reply
    mock_retweet = Mock()
    mock_retweet.retweeted_status = Mock()
    
    mock_reply = Mock()
    mock_reply.in_reply_to_status_id = '456'
    
    # Configure mock search results
    mock_tweepy['api_instance'].search_tweets.return_value = [mock_retweet, mock_reply]
    
    # Run the method
    twitter_bot.reply_to_tweets(
        search_terms=['#test'],
        reply_text='Text reply',
        max_tweets=2
    )
    
    # Verify no replies were attempted
    mock_tweepy['api_instance'].update_status.assert_not_called()
