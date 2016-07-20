import praw
import json
import requests
import tweepy
import time
import os
import urlparse
from glob import glob
from imgurpython import ImgurClient
from imgurpython.helpers.error import ImgurClientError
import sys
from cachetools import LRUCache
import atexit
import pickle
from tokens import *
from whitelist import *

reload(sys)
sys.setdefaultencoding('utf8')

# seconds between updates
WAIT_TIME = 60 * 3
SAVE_FREQUENCY = 6

# Place the name of the folder where the images are downloaded
IMAGE_DIR = 'img'

# Place the name of the file to store the IDs of posts that have been posted
POSTED_CACHE = LRUCache(maxsize = 128)
CACHE_FILE = "cache.pkl"

# Maximum threshold required for momentum posts
THRESHOLD = 50
LAST_TWEET = 0

# Imgur client
IMGUR_CLIENT = ImgurClient(IMGUR_CLIENT_ID, IMGUR_CLIENT_SECRET)

# Twitter API
TWITTER_AUTH_HANDLER = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
TWITTER_AUTH_HANDLER.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
TWITTER_API = tweepy.API(TWITTER_AUTH_HANDLER)

# logging
LOG = open("messages", 'a') 

def setup_connection_reddit(subreddit):
    ''' Creates a c/#onnection to the reddit API. '''
    print('[bot] Setting up connection with reddit')
    reddit_api = praw.Reddit('reddit Twitter tool monitoring {}'.format(subreddit))
    subreddit = reddit_api.get_subreddit(subreddit)
    return subreddit

def should_post(post):
    if (post.stickied):
        return True

    now = time.time()
    elapsed_time = now - LAST_TWEET
    age = now - post.created_utc
    print("[bot] %f" % ((post.score + post.num_comments) / age * elapsed_time))
    if ((post.score + post.num_comments) / age * elapsed_time > THRESHOLD):
        return True
    else:
        return False

def tweet_creator(subreddit_info):
    print('[bot] Getting posts from reddit')

    post = {}
    posts = subreddit_info.get_hot(limit=25)
    try:
        posts = list(posts)
    except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout, praw.errors.HTTPException) as e:
        print(e.message)
        return None

    for p in posts:
        if not already_tweeted(p.id) and should_post(p):
            post['id'] = p.id
            post['title'] = p.title
            post['link'] = "https://redd.it/%s" % p.id
            post['img_path'] = get_image(p.url)
            post['stickied'] = p.stickied
            return post

    return None


def already_tweeted(pid):
    ''' Checks if the reddit Twitter bot has already tweeted a post. '''
    if pid in POSTED_CACHE:
        return True
    else:
        return False


def process_title(title, num_characters, is_esports=True):
    ''' Shortens the title of the post to the 140 character limit. '''

    print("[bot] old title: " + title)
    if len(title) > num_characters:
        title = title[:num_characters] + '...'

    if is_esports:
        for re in PLAYERS:
            title = re.sub("@" + PLAYERS_TO_HANDLE[REVERSE.match(re.pattern).group(1)], title, count=1)

        for re in ORGS:
            title = re.sub("@" + ORGS_TO_HANDLE[REVERSE.match(re.pattern).group(1)], title, count=1)

        for re in PERSONALITIES:
            title = re.sub("@" + PERSONALITIES_TO_HANDLE[REVERSE.match(re.pattern).group(1)], title, count=1)

    if (title[0] == '@'):
	title = "." + title

    print("[bot] new title: " + title)
    return title[:115]

def download_image(url, path):
    print('[bot] Downloading image at URL ' + url + ' to ' + path)
    resp = requests.get(url, stream=True)
    if resp.status_code == 200:
        with open(path, 'wb') as image_file:
            for chunk in resp:
                image_file.write(chunk)
        return path
    else:
        print('[bot] Image failed to download %s. Status code: %s' % (url, str(resp.status_code)))



def get_image(url):
    ''' Downloads i.imgur.com images that reddit posts may point to. '''
    if 'imgur' not in url:
        print('[bot] %s doesn\'t point to an i.imgur.com link' % url)
        return ''

    if 'gifv' in url:
        print('[bot] cannot handle gifv links')
        return ''

    img = None
    try:
        if '/a/' in url:
            # pick first picture in the case of an album
            album_id = os.path.basename(urlparse.urlsplit(url).path)
            img_id = IMGUR_CLIENT.get_album(album_id).cover
            img = IMGUR_CLIENT.get_image(img_id)
        else:
            img_id = os.path.basename(urlparse.urlsplit(url).path).split(".")[0]
            img = IMGUR_CLIENT.get_image(img_id)
    except ImgurClientError as e:
        print('[bot] Image failed to download %s. Status code: %s' % (url, str(e.status_code)))
        print(e.error_message)

    if (img.size > 3072 * 1000):
        return ''

    save_path = IMAGE_DIR + '/' + os.path.basename(urlparse.urlsplit(img.link).path)
    download_image(img.link, save_path)
    return save_path


def tweet(post):
    img_path = post['img_path']

    status = None
    if img_path:
        post_text = process_title(post['title'], 80) + ' #dota2 ' + post['link']
        print('[bot] Posting this link on Twitter')
        print(post_text)
        print('[bot] With image ' + img_path)
        status = TWITTER_API.update_with_media(filename=img_path, status=post_text)
    else:
        post_text = process_title(post['title'], 106) + ' #dota2 ' + post['link']
        print('[bot] Posting this link on Twitter')
        print(post_text)
        status = TWITTER_API.update_status(status=post_text)

    log_tweet(post, status.id)


def log_tweet(post, tweet_id):
    ''' Takes note of when the reddit Twitter bot tweeted a post. '''
    POSTED_CACHE[post['id']] = tweet_id
    global LAST_TWEET
    if not post['stickied']:
        LAST_TWEET = time.time()


def main():
    ''' Runs through the bot posting routine once. '''
    # If the tweet tracking file does not already exist, create it
    if not os.path.exists(IMAGE_DIR):
        os.makedirs(IMAGE_DIR)

    global POSTED_CACHE
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'rb') as cache:
            POSTED_CACHE = pickle.load(cache)
    else:
        POSTED_CACHE = LRUCache(maxsize = 128)

    def save_cache():
        with open(CACHE_FILE, 'wb') as cache:
            pickle.dump(POSTED_CACHE, cache)

    def on_exit():
        # Clean out the image cache
        for filename in glob(IMAGE_DIR + '/*'):
    	    os.remove(filename)

        # save LRU cache to file
        save_cache()

	# close log file
	LOG.close()

    atexit.register(on_exit)

    subreddit = setup_connection_reddit(SUBREDDIT)
    i = 0
    while(True):
        post = tweet_creator(subreddit)
        if post == None:
            time.sleep(WAIT_TIME)
        else:
            try:
                tweet(post)
            except tweepy.error.TweepError as e:
                print("[bot] " + str(e))
                LOG.write("[bot] " + str(e) + "\n")
    		log_tweet(post, "NOT_POSTED")

            time.sleep(WAIT_TIME * 3)
            i += 1

        if (i == SAVE_FREQUENCY):
            save_cache()
            i = 0

if __name__ == '__main__':
    main()
