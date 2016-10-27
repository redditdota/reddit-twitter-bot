import praw
import json
import requests
import twitter
import time
import os
import urllib.parse
import itertools
from glob import glob
from imgurpython import ImgurClient
from imgurpython.helpers.error import ImgurClientError
from gfycat.client import GfycatClient
from gfycat.error import GfycatClientError
import sys
from cachetools import LRUCache
import atexit
import pickle
from tokens import *
from whitelist import *

# seconds between updates
WAIT_TIME = 60 * 3
SAVE_FREQUENCY = 6
HASHTAG = "#dota2"

# Place the name of the folder where the images are downloaded
IMAGE_DIR = "img"
SUPPORTED_IMAGE_TYPES = ("jpg", "jpeg", "png", "gif", "mp4")
MAX_IMAGE_SIZE = 5e6
MAX_FRAME_RATE = 40

# Place the name of the file to store the IDs of posts that have been posted
POSTED_CACHE = LRUCache(maxsize = 128)
CACHE_FILE = "cache.pkl"

# Maximum threshold required for momentum posts
THRESHOLD = 0.59
LAST_TWEET = 0

# Imgur client
IMGUR_CLIENT = ImgurClient(IMGUR_CLIENT_ID, IMGUR_CLIENT_SECRET)

# GFYCHAT client
GFYCAT_CLIENT = GfycatClient()

# Twitter API
TWITTER_API = twitter.Api(consumer_key=TWITTER_CONSUMER_KEY,
                          consumer_secret=TWITTER_CONSUMER_SECRET,
                          access_token_key=TWITTER_ACCESS_TOKEN,
                          access_token_secret=TWITTER_ACCESS_TOKEN_SECRET)

# logging
LOG = open("messages", "a")

def setup_connection_reddit(subreddit):
    """ Creates a c/#onnection to the reddit API. """
    print("[bot] Setting up connection with reddit")
    reddit_api = praw.Reddit("reddit Twitter tool monitoring {}".format(subreddit))
    subreddit = reddit_api.get_subreddit(subreddit)
    return subreddit

def should_post(post):
    if post.over_18:
        return False

    if post.stickied:
        return True

    if post.score <= 3 or post.num_comments <= 10:
        return False

    now = time.time()
    elapsed_time = now - LAST_TWEET
    age = now - post.created_utc
    score = (post.score + 2 * post.num_comments) / (age ** 1.4) * elapsed_time

    if (has_image(post.url)):
        score *= 1.5

    print("[bot] %f" % score)
    if (score > THRESHOLD):
        return True
    else:
        return False

def tweet_creator(subreddit_info):
    print("[bot] Getting posts from reddit")

    post = {}
    posts = itertools.chain(subreddit_info.get_hot(limit=30), subreddit_info.get_rising(limit=1))
    try:
        posts = list(posts)
    except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout, praw.errors.HTTPException) as e:
        print(e)
        return None

    for p in posts:
        if not already_tweeted(p.id) and should_post(p):
            post["id"] = p.id
            post["title"] = p.title
            post["link"] = "https://redd.it/%s" % p.id
            post["img_path"] = get_image(p.url)
            post["video"] = p.url if is_video(p.url) else None
            post["stickied"] = p.stickied
            post["flair"] = p.link_flair_text or ""
            return post

    return None


def already_tweeted(pid):
    """ Checks if the reddit Twitter bot has already tweeted a post. """
    if pid in POSTED_CACHE:
        return True
    else:
        return False

def process_title(post):
    """ Shortens the title of the post to the 140 character limit. """

    print("[bot] raw title: " + post["title"])

    title = post["title"]
    #is_esports = "esports" in post["flair"].lower()
    is_esports = True
    title_lower = title.lower()
    if is_esports and \
        ("shop" not in title_lower) and \
        ("moon shard" not in title_lower) and \
        ("black king bar" not in title_lower) and \
        ("black hole" not in title_lower):
        for player in PLAYERS:
            title = player.sub("@" + PLAYERS_TO_HANDLE[REVERSE.match(player.pattern).group(1)], title, count=1)

        for org in ORGS:
            title = org.sub("@" + ORGS_TO_HANDLE[REVERSE.match(org.pattern).group(1)], title, count=1)

        for people in PERSONALITIES:
            title = people.sub("@" + PERSONALITIES_TO_HANDLE[REVERSE.match(people.pattern).group(1)], title, count=1)

    title = title.strip()
    if (title[0] == "@"):
        title = "." + title

    max_length = 140 - 3
    if post["video"]:
        suffix = " " + post["link"] + ". " + HASHTAG + " " + post["video"]
        max_length -= (4 + len(HASHTAG) + 23 * 2)
    elif post["img_path"]:
        suffix = " " + post["link"] + ". " + HASHTAG
        max_length -= (3 + len(HASHTAG) + 23)
    else:
        suffix = " " + HASHTAG + " " + post["link"]
        max_length -= (2 + len(HASHTAG) + 23)

    shortened = False
    # shortening to 140
    while (len(title) > max_length):
        shortened = True
        idx = title.rfind(" ")
        if (title[idx] == "@"):
            title = title[:idx]
        else:
            title = title[:max_length]

    if (shortened):
        title = title + "..."

    title = title + suffix
    print("[bot] new title: " + title)
    return title

def download_image(url, path):
    print("[bot] Downloading image at URL " + url + " to " + path)
    resp = requests.get(url, stream=True)
    if resp.status_code == 200:
        try:
            with open(path, "wb") as image_file:
                for chunk in resp:
                    image_file.write(chunk)
            return path
        except IOError as e:
            print("[bot] Image failed to download %s." % url)
            print(e.error_message)
            cleanup_images()
            return None
    else:
        print("[bot] Image failed to download %s. Status code: %s" % (url, str(resp.status_code)))


def has_image(url):
    if is_direct_link(url):
        return True

    if "imgur" in url:
        return True

    if "gfycat" in url:
        return True

    if "gifv" in url:
        #print("[bot] cannot handle gifv links")
        return False

    return False

def is_direct_link(url):
    return url.endswith(SUPPORTED_IMAGE_TYPES)

def get_imgur_link(url):
    print("[bot] downloading from imgur")
    img = None
    try:
        if "/a/" in url:
            # pick first picture in the case of an album
            album_id = os.path.basename(urllib.parse.urlsplit(url).path)
            img_id = IMGUR_CLIENT.get_album(album_id).cover
            img = IMGUR_CLIENT.get_image(img_id)
        else:
            img_id = os.path.basename(urllib.parse.urlsplit(url).path).split(".")[0]
            img = IMGUR_CLIENT.get_image(img_id)
    except ImgurClientError as e:
        print("[bot] Image failed to download %s. Status code: %s" % (url, str(e.status_code)))
        print(e.error_message)
        return None

    if not img.type.endswith(SUPPORTED_IMAGE_TYPES):
        return None

    if img.animated:
        if (img.size > MAX_IMAGE_SIZE):
            if (img.mp4_size > MAX_IMAGE_SIZE):
                print("[bot] animated image %s too large" % url)
                return None
            else:
                return img.mp4
        else:
            return img.link
    else:
        if (img.size > 5e6):
            print("[bot] image %s too large" % url)
            return None

    return img.link

def get_gfycat_link(url):
    assert("gfycat" in url.lower())
    name = url.split("/")[-1]
    gfy = None
    try:
        gfy = GFYCAT_CLIENT.query_gfy(name)
    except GfycatClientError as e:
        print("[bot] Gfycat error: could not query %s" % url)
        print(e.error_message)
        print(e.status_code)
        return None

    if "error" in gfy or "gfyItem" not in gfy:
        print("[bot] Gfycat error: could not query %s" % url)
        return None
    else:
        gfy = gfy["gfyItem"]

    link = ""
    if "gifUrl" in gfy and int(gfy["gifSize"]) <= MAX_IMAGE_SIZE:
        link = gfy["gifUrl"]
    else:
        if int(gfy["frameRate"]) < MAX_FRAME_RATE and "mp4Url" in gfy:
            if int(gfy["mp4Size"]) <= MAX_IMAGE_SIZE * 3:
                link = gfy["mp4Url"]
            else:
                link = gfy["mobileUrl"]
        else:
            link = gfy.get("max5mbGif", None)

    if link and link.endswith(SUPPORTED_IMAGE_TYPES):
        return link
    else:
        return None

def get_image(url):
    """ Downloads i.imgur.com images that reddit posts may point to. """
    if not has_image(url):
        return None

    link = ""
    if "imgur" in url:
        link = get_imgur_link(url)
    elif "gfycat" in url:
        link = get_gfycat_link(url)
    elif is_direct_link(url):
        link = url

    if link is None:
        return None

    save_path = IMAGE_DIR + "/" + os.path.basename(urllib.parse.urlsplit(link).path)
    download_image(link, save_path)
    return save_path

def is_video(link):
    return any(site in link.lower() for site in ("youtube", "twitch", "oddshot"))

def tweet(post):
    img_path = post["img_path"]

    # spoiler protection
    if "esports" in post["flair"].lower() \
        and ("congrat" in post["title"].lower() or "winner" in post["title"].lower()):
        img_path = "victory.jpeg"

    status = None
    if img_path:
        post_text = process_title(post)
        print("[bot] Posting this link on Twitter")
        print(post_text)
        print("[bot] With image " + img_path)
        status = TWITTER_API.PostUpdate(media=img_path, status=post_text)
    else:
        post_text = process_title(post)
        print("[bot] Posting this link on Twitter")
        print(post_text)
        status = TWITTER_API.PostUpdate(status=post_text)

    log_tweet(post, status.id)


def log_tweet(post, tweet_id):
    """ Takes note of when the reddit Twitter bot tweeted a post. """
    POSTED_CACHE[post["id"]] = tweet_id
    global LAST_TWEET
    if not post["stickied"]:
        LAST_TWEET = time.time()

def cleanup_images():
    # Clean out the image cache
    for filename in glob(IMAGE_DIR + "/*"):
        os.remove(filename)


def main():
    """ Runs through the bot posting routine once. """
    # If the tweet tracking file does not already exist, create it
    if not os.path.exists(IMAGE_DIR):
        os.makedirs(IMAGE_DIR)

    global POSTED_CACHE
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "rb") as cache:
            POSTED_CACHE = pickle.load(cache)
    else:
        POSTED_CACHE = LRUCache(maxsize = 128)

    def save_cache():
        with open(CACHE_FILE, "wb") as cache:
            pickle.dump(POSTED_CACHE, cache)

        for filename in glob(IMAGE_DIR + "/*"):
            os.remove(filename)

    def on_exit():
        cleanup_images()
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
            except twitter.error.TwitterError as e:
                print("[bot] " + str(e))
                LOG.write("[bot] " + str(e) + "\n")
                log_tweet(post, "NOT_POSTED")

            time.sleep(WAIT_TIME * 3)
            i += 1

        if (i == SAVE_FREQUENCY):
            save_cache()
            cleanup_images()
            i = 0

if __name__ == "__main__":
    main()
