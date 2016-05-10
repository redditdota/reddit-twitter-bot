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
from tokens import *
import sys

reload(sys)
sys.setdefaultencoding('utf8')

# seconds to wait in between posts
WAIT_TIME = 60 * 30

# Place the name of the folder where the images are downloaded
IMAGE_DIR = 'img'

# Place the name of the file to store the IDs of posts that have been posted
POSTED_CACHE = 'posted_posts.txt'

# Imgur client
IMGUR_CLIENT = ImgurClient(IMGUR_CLIENT_ID, IMGUR_CLIENT_SECRET)

def setup_connection_reddit(subreddit):
    ''' Creates a c/#onnection to the reddit API. '''
    print('[bot] Setting up connection with reddit')
    reddit_api = praw.Reddit('reddit Twitter tool monitoring {}'.format(subreddit))
    subreddit = reddit_api.get_subreddit(subreddit)
    return subreddit


def tweet_creator(subreddit_info):
    last_post = None 
    ''' Looks up posts from reddit and shortens the URLs to them. '''
    post_dict = {}

    print('[bot] Getting posts from reddit')

    # You can use the following "get" functions to get posts from reddit:
    #   - get_top(): gets the most-upvoted posts (ignoring post age)
    #   - get_hot(): gets the most-upvoted posts (taking post age into account)
    #   - get_new(): gets the newest posts
    #
    # "limit" tells the API the maximum number of posts to look up

    while (len(post_dict) < 3):
        posts = []
        if last_post is None:
            posts = subreddit_info.get_hot(limit=3)
        else:
            posts = subreddit_info.get_hot(limit=3, params={"after": last_post})

        for p in posts:
            if not already_tweeted(p.id):
                # This stores a link to the reddit post itself
                # If you want to link to what the post is linking to instead, use
                # "p.url" instead of "p.permanlink"
                post_dict[p.id] = {}
                post = post_dict[p.id]
                post['title'] = p.title
                post['link'] = p.permalink

                # Store the url the post points to (if any)
                # If it's an imgur URL, it will later be downloaded and uploaded alongside the tweet
                post['img_path'] = get_image(p.url)
            else:
                print('[bot] Already tweeted: {}'.format(str(p)))

            last_post = p.fullname

    return post_dict


def already_tweeted(pid):
    ''' Checks if the reddit Twitter bot has already tweeted a post. '''
    found = False
    with open(POSTED_CACHE, 'r') as in_file:
        for line in in_file:
            if pid in line:
                found = True
                break
    return found


def strip_title(title, num_characters):
    ''' Shortens the title of the post to the 140 character limit. '''

    # How much you strip from the title depends on how much extra text
    # (URLs, hashtags, etc.) that you add to the tweet
    if len(title) <= num_characters:
        return title
    else:
        return title[:num_characters] + '…'

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

    img_url = ''
    try:
        if 'i.imgur.com' in url:
            img_url = url
        elif '/a/' in url:
            # pick first picture in the case of an album
            album_id = os.path.basename(urlparse.urlsplit(url).path)
            img_id = IMGUR_CLIENT.get_album(album_id).cover
            img_url = IMGUR_CLIENT.get_image(img_id).link
        else:
            img_id = os.path.basename(urlparse.urlsplit(url).path)
            img_url = IMGUR_CLIENT.get_image(img_id).link
    except ImgurClientError as e:
        print('[bot] Image failed to download %s. Status code: %s' % (url, str(e.status_code)))
        print(e.error_message)

    save_path = IMAGE_DIR + '/' + os.path.basename(urlparse.urlsplit(img_url).path)
    download_image(img_url, save_path)
    return save_path


def tweeter(post_dict):
    ''' Tweets all of the selected reddit posts. '''
    auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
    auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)

    print post_dict
    for pid in post_dict:
        post = post_dict[pid]
        img_path = post_dict[pid]['img_path']

        if img_path:
            post_text = strip_title(post['title'], 83) + ' ' + post['link'] + ' #dota2'
            print('[bot] Posting this link on Twitter')
            print(post_text)
            print('[bot] With image ' + img_path)
            api.update_with_media(filename=img_path, status=post_text)
        else:
            post_text = strip_title(post['title'], 106) + ' ' + post['link'] + ' #dota2'
            print('[bot] Posting this link on Twitter')
            print(post_text)
            api.update_status(status=post_text)
        log_tweet(pid)
        time.sleep(WAIT_TIME)


def log_tweet(pid):
    ''' Takes note of when the reddit Twitter bot tweeted a post. '''
    with open(POSTED_CACHE, 'a') as out_file:
        out_file.write(str(pid) + '\n')


def main():
    ''' Runs through the bot posting routine once. '''
    # If the tweet tracking file does not already exist, create it
    if not os.path.exists(POSTED_CACHE):
        with open(POSTED_CACHE, 'w'):
            pass
    if not os.path.exists(IMAGE_DIR):
        os.makedirs(IMAGE_DIR)

    subreddit = setup_connection_reddit(SUBREDDIT)
    while(True):
        post_dict = tweet_creator(subreddit)
        tweeter(post_dict)

    # Clean out the image cache
    for filename in glob(IMAGE_DIR + '/*'):
    	os.remove(filename)

if __name__ == '__main__':
    main()
