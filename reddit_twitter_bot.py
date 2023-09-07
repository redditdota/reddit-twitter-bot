import atexit
import itertools
import json
import logging
import os
import pickle
import sys
import time
import urllib.error
import urllib.parse
from glob import glob
from random import randint

import praw
import requests
import tweepy
from cachetools import LRUCache
from imgurpython import ImgurClient
from imgurpython.helpers.error import ImgurClientError, ImgurClientRateLimitError
from PIL import Image

from tokens import *
from whitelist import *

logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)

# seconds between updates
WAIT_TIME = 60 * 15
SAVE_FREQUENCY = 6
MAX_TRIES = 5

# Place the name of the folder where the images are downloaded
IMAGE_DIR = "img"
SUPPORTED_IMAGE_TYPES = ("jpg", "jpeg", "png", "gif", "mp4")
MAX_IMAGE_SIZE = 5e6
MAX_FRAME_RATE = 40

# Place the name of the file to store the IDs of posts that have been posted
POSTED_CACHE = LRUCache(maxsize=128)
CACHE_FILE = None

# Maximum threshold required for momentum posts
THRESHOLD = 0.5
LAST_TWEET = 0

# Imgur client
IMGUR_CLIENT = ImgurClient(IMGUR_CLIENT_ID, IMGUR_CLIENT_SECRET)

# Twitter API
TWITTER_API = None
TWITTER_CLIENT = None
HASHTAG = None

# logging
LOG = open("messages", "a")


def setup_connection_reddit(subreddit):
    """Creates a c/#onnection to the reddit API."""
    logging.info("Setting up connection with reddit")
    reddit_api = praw.Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_CLIENT_SECRET,
        user_agent="reddit Twitter tool monitoring {}".format(subreddit),
    )
    subreddit = reddit_api.subreddit(subreddit)
    return subreddit


def should_post(post):
    if post.over_18:
        return False

    if post.stickied:
        return True

    if post.score + post.num_comments <= 40:
        return False

    now = time.time()
    elapsed_time = now - LAST_TWEET
    age = now - post.created_utc

    if age > 1 * 3600:
        return True

    score = (1.3 * post.score + post.num_comments) / (age**1.4) * elapsed_time

    if has_image(post.url):
        score *= 1.5

    logging.info("%f" % score)
    if score > THRESHOLD:
        return True
    else:
        return False


def tweet_creator(subreddit_info):
    logging.info("Getting posts from reddit")

    posts = itertools.chain(
        subreddit_info.hot(limit=35), subreddit_info.rising(limit=3)
    )
    try:
        posts = list(posts)
    except Exception as e:
        logging.info(e)
        return None

    post = {}
    for p in posts:
        if not already_tweeted(p.id) and should_post(p):
            post["id"] = p.id
            post["title"] = p.title
            post["author"] = p.author.name
            post["link"] = "https://redd.it/%s" % p.id
            post["img_paths"] = get_images(p.url)
            post["url"] = p.url if is_video(p.url) or "twitter" in p.url else None
            post["stickied"] = p.stickied
            post["flair"] = p.link_flair_text or ""
            post["spoiler"] = p.spoiler
            return post

    return None


def already_tweeted(pid):
    """Checks if the reddit Twitter bot has already tweeted a post."""
    if pid in POSTED_CACHE:
        return True
    else:
        return False


def _substitute_handles(title):
    for b in BLACK_LIST:
        if b in title:
            return title

    for (handle, names) in PLAYERS.items():
        for name in names:
            if re.search(name, title) is not None:
                title = name.sub(r"\1@{}\3".format(handle), title, count=1)
                break

    for (handle, names) in ARTIFACT.items():
        for name in names:
            if re.search(name, title) is not None:
                title = name.sub(r"\1@{}\3".format(handle), title, count=1)
                break

    for (handle, names) in ORGS.items():
        for name in names:
            if re.search(name, title) is not None:
                title = name.sub(r"\1@{}\3".format(handle), title, count=1)
                break

    for (handle, names) in PERSONALITIES.items():
        for name in names:
            if re.search(name, title) is not None:
                title = name.sub(r"\1@{}\3".format(handle), title, count=1)
                break

    return title


def process_title(post):
    """Shortens the title of the post to the 140 character limit."""

    logging.info("raw title: " + post["title"])

    title = _substitute_handles(post["title"]).strip()
    author = f" - /u/{post['author']} "
    if title[0] == "@":
        title = "." + title

    max_length = 279 - 3
    if post["url"]:
        suffix = author + post["link"] + " " + HASHTAG + " " + post["url"]
        max_length -= 4 + len(HASHTAG) + 23 * 2
    elif post["img_paths"]:
        suffix = author + post["link"] + " " + HASHTAG
        max_length -= 3 + len(HASHTAG) + 23
    else:
        suffix = author + HASHTAG + " " + post["link"]
        max_length -= 2 + len(HASHTAG) + 23

    max_length -= len(author)

    shortened = False
    # shortening to 279
    while len(title) > max_length:
        shortened = True
        idx = title.rfind(" ")
        if idx > 0:
            title = title[:idx]
        else:
            title = title[:max_length]

    if shortened:
        title = title + "..."

    title = title + suffix
    logging.info("new title: " + title)
    return title


def download_image(url, path):
    logging.info("Downloading image at URL " + url + " to " + path)
    resp = requests.get(url, stream=True)
    if resp.status_code == 200:
        try:
            with open(path, "wb") as image_file:
                for chunk in resp:
                    image_file.write(chunk)
            return path
        except IOError as e:
            logging.info("Image failed to download %s." % url)
            logging.info(e.error_message)
            cleanup_images()
            return None
    else:
        logging.info(
            "Image failed to download %s. Status code: %s"
            % (url, str(resp.status_code))
        )
        return None


def has_image(url):
    if is_direct_link(url):
        return True

    if "imgur" in url:
        return True

    if "reddituploads" in url:
        return True

    if "gifv" in url:
        # logging.info("cannot handle gifv links")
        return False

    return False


def is_direct_link(url):
    return url.endswith(SUPPORTED_IMAGE_TYPES)


def process_imgur_link(img):
    if not img.type.endswith(SUPPORTED_IMAGE_TYPES):
        return None

    if img.animated:
        if img.size > MAX_IMAGE_SIZE:
            if img.mp4_size > MAX_IMAGE_SIZE:
                logging.info("animated image %s too large" % img.link)
                return None
            else:
                return img.mp4
        else:
            return img.link
    else:
        if img.size > 5e6:
            logging.info("image %s too large" % img.link)
            return None

    return img.link


def get_imgur_links(url, attempts=0):
    try:
        return get_imgur_links_helper(url)
    except ImgurClientRateLimitError:
        if attempts < MAX_TRIES:
            time.sleep(30)
            return get_imgur_links(url, attempts + 1)
        else:
            return []


def get_imgur_links_helper(url):
    logging.info("downloading from imgur")
    imgs = []
    img_id = ""
    if "/a/" in url or "gallery" in url:
        img_id = os.path.basename(urllib.parse.urlsplit(url).path)
    else:
        img_id = os.path.basename(urllib.parse.urlsplit(url).path).split(".")[0]

    try:
        album = IMGUR_CLIENT.get_album(img_id)
        for image in album.images:
            img_link = process_imgur_link(IMGUR_CLIENT.get_image(image["id"]))
            if img_link:
                imgs.append(img_link)
                if img_link.endswith(("gif", "mp4")):
                    break

            if len(imgs) >= 4:
                break
    except ImgurClientError as e:
        try:
            img_link = process_imgur_link(IMGUR_CLIENT.get_image(img_id))
            imgs = [img_link] if img_link else []
        except ImgurClientError as e:
            logging.info(
                "Image failed to download %s. Status code: %s"
                % (url, str(e.status_code))
            )
            logging.info(e.error_message)
            return []

    logging.info(imgs)
    return imgs




def get_images(url):
    """Downloads i.imgur.com images that reddit posts may point to."""
    if not has_image(url):
        return None

    links = []
    if "imgur" in url:
        links = get_imgur_links(url)
    elif is_direct_link(url):
        links = [url]
    elif "reddituploads" in url:
        links = [url]

    if len(links) == 0:
        return None

    save_paths = []
    for link in links:
        save_path = IMAGE_DIR + "/" + os.path.basename(urllib.parse.urlsplit(link).path)
        if download_image(link, save_path) is not None:
            save_paths.append(save_path)
    if len(save_paths) > 0:
        return save_paths
    else:
        return None


def is_video(link):
    return any(site in link.lower() for site in ("youtube", "twitch", "oddshot"))


def is_spoiler(post):
    if post["spoiler"]:
        return True

    title_lower = post["title"].lower()
    if "congrat" in title_lower:
        return True

    if "winner" in title_lower and "bracket" not in title_lower:
        return True

    if "post" in title_lower and "match" in title_lower:
        return True

    return False


def upload_image(paths):
    ids = []
    for path in paths:
        # twitter image size limitations (https://developer.twitter.com/en/docs/twitter-api/v1/media/upload-media/uploading-media/media-best-practices)
        if os.stat(path).st_size / 1e6 > 512:
            continue

        with Image.open(path) as im:
            (w, h) = im.size
            if w > 1280 or h > 1024:
                continue

        try:
            media = TWITTER_API.media_upload(filename=path)
            ids.append(media.media_id_string)
        except urllib.error.URLError as e:
            logging.info("" + str(e))
            LOG.write("" + str(e) + "\n")

    if len(ids) == 0:
        return None
    else:
        return ids


def tweet(post):
    img_paths = post["img_paths"]

    # spoiler protection
    # if "esports" in post["flair"].lower() and is_spoiler(post["title"]):
    if img_paths is None and post["url"] is None and is_spoiler(post):
        img_paths = ["victory/%d.gif" % randint(0, 10)]

    status = None
    if img_paths and len(img_paths) > 0:
        post_text = process_title(post)
        logging.info("Posting this link on Twitter")
        logging.info(post_text)
        logging.info("With images " + str(img_paths))
        media_ids = upload_image(img_paths)
        status = TWITTER_CLIENT.create_tweet(text=post_text, media_ids=media_ids)
    else:
        post_text = process_title(post)
        logging.info("Posting this link on Twitter")
        logging.info(post_text)
        status = TWITTER_CLIENT.create_tweet(text=post_text)

    log_tweet(post, status)


def log_tweet(post, tweet_id):
    """Takes note of when the reddit Twitter bot tweeted a post."""
    if tweet_id == "NOT_POSTED":
        return

    POSTED_CACHE[post["id"]] = tweet_id
    global LAST_TWEET
    if not post["stickied"]:
        LAST_TWEET = time.time()


def cleanup_images():
    # Clean out the image cache
    for filename in glob(IMAGE_DIR + "/*"):
        os.remove(filename)


def main():
    assert len(sys.argv) == 2
    global SUBREDDIT
    SUBREDDIT_FILE = sys.argv[1]
    token = __import__(SUBREDDIT_FILE)
    SUBREDDIT = token.SUBREDDIT

    auth = tweepy.OAuth1UserHandler(
        consumer_key=token.TWITTER_CONSUMER_KEY,
        consumer_secret=token.TWITTER_CONSUMER_SECRET,
        access_token=token.TWITTER_ACCESS_TOKEN,
        access_token_secret=token.TWITTER_ACCESS_TOKEN_SECRET,
    )

    global TWITTER_API
    TWITTER_API = tweepy.API(auth)

    global TWITTER_CLIENT
    TWITTER_CLIENT = tweepy.Client(
        bearer_token=token.TWITTER_BEARER_TOKEN,
        consumer_key=token.TWITTER_CONSUMER_KEY,
        consumer_secret=token.TWITTER_CONSUMER_SECRET,
        access_token=token.TWITTER_ACCESS_TOKEN,
        access_token_secret=token.TWITTER_ACCESS_TOKEN_SECRET,
    )

    # global UPLOAD
    # UPLOAD = twitter.Twitter(domain="upload.twitter.com", auth=auth)

    global HASHTAG
    HASHTAG = "#" + token.HASHTAG

    """ Runs through the bot posting routine once. """
    # If the tweet tracking file does not already exist, create it
    if not os.path.exists(IMAGE_DIR):
        os.makedirs(IMAGE_DIR)

    if not os.path.exists("cache"):
        os.makedirs("cache")

    global CACHE_FILE
    CACHE_FILE = "cache/%s.pkl" % SUBREDDIT
    global POSTED_CACHE
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "rb") as cache:
            POSTED_CACHE = pickle.load(cache)
    else:
        POSTED_CACHE = LRUCache(maxsize=128)

    def save_cache():
        with open(CACHE_FILE, "wb") as cache:
            pickle.dump(POSTED_CACHE, cache)

    def on_exit():
        cleanup_images()
        # save LRU cache to file
        save_cache()
        # close log file
        LOG.close()

    atexit.register(on_exit)

    subreddit = setup_connection_reddit(SUBREDDIT)
    i = 0
    while True:
        post = tweet_creator(subreddit)
        if post == None:
            time.sleep(WAIT_TIME)
        else:
            try:
                tweet(post)
            except requests.exceptions.ConnectionError as e:
                logging.info("" + str(e))
                LOG.write("" + str(e) + "\n")
                log_tweet(post, "NOT_POSTED")
            except tweepy.errors.BadRequest as e:
                logging.info("" + str(e))
                LOG.write("" + str(e) + "\n")
                log_tweet(post, "NOT_POSTED")

            time.sleep(WAIT_TIME * 2)
            save_cache()
            i += 1

        if i == SAVE_FREQUENCY:
            cleanup_images()
            i = 0


if __name__ == "__main__":
    main()
