# r/Dota2 Twitter Bot

## Setup

Install pipenv

```sh
pip install --user pipenv
```

Create python virtual environment

```sh
pipenv install --dev
```

## Required Tokens

API tokens in tokens.py:

```text
# Imgur API keys
IMGUR_CLIENT_ID = ...
IMGUR_CLIENT_SECRET = ...

# Reddit API keys
REDDIT_CLIENT_SECRET = ...
REDDIT_CLIENT_ID = ...

# Gfycat API keys
GFYCAT_CLIENT_ID = ...
GFYCAT_CLIENT_SECRET = ...
```

Subreddit specific tokens in dota2.py:

```text

# Twitter API keys
TWITTER_ACCESS_TOKEN = ...
TWITTER_ACCESS_TOKEN_SECRET = ...
TWITTER_CONSUMER_KEY = ...
TWITTER_CONSUMER_SECRET = ...

# Place the subreddit you want to look up posts from here
SUBREDDIT = 'dota2'
HASHTAG = '#dota2'
```

## Running the bot

```sh
python reddit_twitter_bot.py dota2
```