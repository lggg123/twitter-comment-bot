# Twitter Comment Bot

A Python-based Twitter bot that automatically searches for tweets with specific hashtags and responds to them. Built using Twitter API v2 and Tweepy.

## Features

- Searches for tweets based on configurable hashtags
- Automatically replies to found tweets with customizable messages
- Handles Twitter API rate limits gracefully
- Configurable through YAML files
- Logging system for tracking bot activity

## Prerequisites

- Python 3.11 or higher
- Twitter Developer Account with API access
- Twitter API Keys and Tokens (Essential Access or higher)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/lggg123/twitter-comment-bot.git
cd twitter-comment-bot
```
2. Create and activate a virtual environment:
```bash
bash
python3 -m venv venv_311
source venv_311/bin/activate # On Windows: venv_311\Scripts\activate
```
3. Install the required packages:
```bash
pip3 install -r requirements.txt
```

4. Set up configuration:
   - Create a `config` directory in the project root
   - Create `config.yaml` and `secrets.yaml` files in the `config` directory

5. Configure your Twitter API credentials in `config/secrets.yaml`:
```yaml
twitter:
api_key: "your_api_key_here"
api_secret_key: "your_api_secret_key_here"
access_token: "your_access_token_here"
access_token_secret: "your_access_token_secret_here"
bearer_token: "your_bearer_token_here"
```
## Usage

1. Start the bot:
```bash
python3 test_live.py
```

2. The bot will:
   - Search for tweets containing specified hashtags
   - Reply to found tweets with configured messages
   - Handle rate limits automatically
   - Log all activities

## Rate Limits

Twitter API has rate limits that affect the bot's operation:

- **Essential Access (Free)**:
  - 50 tweets/replies per 24 hours
  - 180 search requests per 15 minutes
  - Automatic rate limit handling with sleep timers

- **Basic Access ($100/month)**:
  - 3,000 tweets/replies per month
  - Higher search request limits
  - More available endpoints

## Configuration

### Search Terms
Modify the search terms in `test_live.py`:
```python
bot.reply_to_tweets(
search_terms=['#python'], # Add your hashtags here
reply_text="Your reply message",
max_tweets=10
)

### Rate Limit Handling
The bot includes built-in rate limit handling:
- Automatic sleep when limits are reached
- Configurable retry delays
- Logging of rate limit events

## Project Structure
twitter_comment_new_bot/
├── config/
│ ├── config.yaml
│ └── secrets.yaml
├── src/
│ ├── init.py
│ ├── bot.py
│ └── config.py
├── logs/
├── requirements.txt
├── test_live.py
└── README.md

## Logging

Logs are stored in the `logs` directory and include:
- Bot initialization
- Tweet searches and replies
- Rate limit events
- Errors and exceptions

## Security Notes

- Never commit `secrets.yaml` to version control
- Keep your API credentials secure
- Use environment variables for production deployments

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

[Your chosen license]

## Disclaimer

This bot is for educational purposes. Ensure compliance with Twitter's Terms of Service and API usage guidelines when deploying.