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
from random import randint
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
THRESHOLD = 0.5
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
    reddit_api = praw.Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_CLIENT_SECRET,
        user_agent="reddit Twitter tool monitoring {}".format(subreddit))
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

    score = (post.score +  post.num_comments) / (age ** 1.4) * elapsed_time

    if (has_image(post.url)):
        score *= 1.5

    print("[bot] %f" % score)
    if score > THRESHOLD:
        return True
    else:
        return False

def tweet_creator(subreddit_info):
    print("[bot] Getting posts from reddit")

    posts = itertools.chain(subreddit_info.hot(limit=30), subreddit_info.rising(limit=3))
    try:
        posts = list(posts)
    except Exception as e:
        print(e)
        return None

    post = {}
    for p in posts:
        if not already_tweeted(p.id) and should_post(p):
            post["id"] = p.id
            post["title"] = p.title
            post["link"] = "https://redd.it/%s" % p.id
            post["img_paths"] = get_images(p.url)
            post["url"] = p.url if is_video(p.url) or "twitter" in p.url else None
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
        ("dark moon" not in title_lower) and \
        ("darkmoon" not in title_lower) and \
        ("moon shard" not in title_lower) and \
        ("shadow demon" not in title_lower) and \
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

    max_length = 139 - 3
    if post["url"]:
        suffix = " " + post["link"] + " " + HASHTAG + " " + post["url"]
        max_length -= (4 + len(HASHTAG) + 23 * 2)
    elif post["img_paths"]:
        suffix = " " + post["link"] + " " + HASHTAG
        max_length -= (3 + len(HASHTAG) + 23)
    else:
        suffix = " " + HASHTAG + " " + post["link"]
        max_length -= (2 + len(HASHTAG) + 23)

    shortened = False
    # shortening to 139
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

    if "reddituploads" in url:
        return True

    if "gifv" in url:
        #print("[bot] cannot handle gifv links")
        return False

    return False

def is_direct_link(url):
    return url.endswith(SUPPORTED_IMAGE_TYPES)

def process_imgur_link(img):
    if not img.type.endswith(SUPPORTED_IMAGE_TYPES):
        return None

    if img.animated:
        if (img.size > MAX_IMAGE_SIZE):
            if (img.mp4_size > MAX_IMAGE_SIZE):
                print("[bot] animated image %s too large" % img.link)
                return None
            else:
                return img.mp4
        else:
            return img.link
    else:
        if (img.size > 5e6):
            print("[bot] image %s too large" % img.link)
            return None

    return img.link

def get_imgur_links(url):
    print("[bot] downloading from imgur")
    imgs = []
    img_id = ""
    if "/a/" in url or 'gallery' in url:
        img_id = os.path.basename(urllib.parse.urlsplit(url).path)
    else:
        img_id = os.path.basename(urllib.parse.urlsplit(url).path).split(".")[0]

    try:
        album = IMGUR_CLIENT.get_album(img_id)
        for image in IMGUR_CLIENT.get_album(img_id).images:
            img_link = process_imgur_link(IMGUR_CLIENT.get_image(image['id']))
            if img_link:
                imgs.append(img_link)
            if len(imgs) >= 4 or img_link.endswith(("gif", "mp4")):
                break
    except ImgurClientError as e:
        try:
            img_link = process_imgur_link(IMGUR_CLIENT.get_image(img_id))
            imgs = [img_link] if img_link else []
        except ImgurClientError as e:
            print("[bot] Image failed to download %s. Status code: %s" % (url, str(e.status_code)))
            print(e.error_message)
            return []

    print(imgs)
    return imgs

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
    if "gifUrl" in gfy and "gifSize" in gfy and int(gfy["gifSize"]) <= MAX_IMAGE_SIZE:
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

def get_images(url):
    """ Downloads i.imgur.com images that reddit posts may point to. """
    if not has_image(url):
        return None

    links = []
    if "imgur" in url:
        links = get_imgur_links(url)
    elif "gfycat" in url:
        links = [get_gfycat_link(url)]
    elif is_direct_link(url):
        links = [url]
    elif "reddituploads" in url:
        links = [url]

    if len(links) == 0:
        return None

    save_paths = []
    for link in links:
        save_path = IMAGE_DIR + "/" + os.path.basename(urllib.parse.urlsplit(link).path)
        download_image(link, save_path)
        save_paths.append(save_path)
    return save_paths

def is_video(link):
    return any(site in link.lower() for site in ("youtube", "twitch", "oddshot"))

def is_spoiler(title):
    title_lower = title.lower()
    if "congrat" in title_lower:
        return True

    if "winner" in title_lower and "bracket" not in title_lower:
        return True

    if "post" in title_lower:
        return True

    return False

def tweet(post):
    img_paths = post["img_paths"]

    # spoiler protection
    #if "esports" in post["flair"].lower() and is_spoiler(post["title"]):
    if img_paths is None and post["url"] is None and is_spoiler(post["title"]):
        img_paths = ["victory/%d.gif" % randint(0, 10)]

    status = None
    if img_paths and len(img_paths) > 0:
        post_text = process_title(post)
        print("[bot] Posting this link on Twitter")
        print(post_text)
        print("[bot] With images " + str(img_paths))
        if len(img_paths) == 1:
            status = TWITTER_API.PostUpdate(media=img_paths[0], status=post_text)
        else:
            status = TWITTER_API.PostUpdate(media=img_paths, status=post_text)
    else:
        post_text = process_title(post)
        print("[bot] Posting this link on Twitter")
        print(post_text)
        status = TWITTER_API.PostUpdate(status=post_text)

    log_tweet(post, status.id)


def log_tweet(post, tweet_id):
    """ Takes note of when the reddit Twitter bot tweeted a post. """
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
                log_tweet(post, "ERROR")
            except requests.exceptions.ConnectionError as e:
                print("[bot] " + str(e))
                LOG.write("[bot] " + str(e) + "\n")
                log_tweet(post, "NOT_POSTED")

            time.sleep(WAIT_TIME * 3)
            save_cache()
            i += 1

        if (i == SAVE_FREQUENCY):
            cleanup_images()
            i = 0

if __name__ == "__main__":
    main()
