import json
from collections import Counter


def read_json(filename):
    with open(filename, encoding="utf-8") as file:
        return json.load(file)


def posts_with_comments_count(POSTS_PATH, COMMENTS_PATH):
    posts = read_json(POSTS_PATH)
    comments = read_json(COMMENTS_PATH)
    comments_num = dict(Counter([x["post_id"] for x in comments]))
    for post in posts:
        for key in comments_num:
            if post["pk"] == key:
                post["comments_count"] = comments_num[key]
        if "comments_count" not in post:
            post["comments_count"] = 0
    return posts


def get_comments_by_post(COMMENTS_PATH, post_id):
    comments = read_json(COMMENTS_PATH)
    return [comment for comment in comments if comment["post_id"] == post_id]


def add_comment(COMMENTS_PATH, comment):
    data = read_json(COMMENTS_PATH)
    data.append(comment)
    with open(COMMENTS_PATH, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4, sort_keys=True)


def get_posts_by_search(data, s):
    results = [post for post in data if s.lower() in post["content"].lower()]
    return results


def get_posts_by_username(data, username):
    results = [post for post in data if username == post["poster_name"]]
    return results


def tags_to_links(data):
    for post in data:
        tags = set()
        content = post["content"]
        words = content.split()
        for word in words:
            if word.startswith("#"):
                tags.add(word)
        for tag in tags:
            words_links = list()
            for word in words:
                if word == tag:
                    word = '<a href="/tag/' + tag[1:] + '">' + tag + "</a>"
                words_links.append(word)
            words = words_links
        post["content"] = " ".join(words)
    return data


def get_posts_by_tag(data, tag):
    results = [post for post in data if "#" + tag in post["content"]]
    return results


def add_bookmark(BOOKMARKS_PATH, postid):
    data = read_json(BOOKMARKS_PATH)
    bookmark = {"postid": postid}
    data.append(bookmark)
    data = list({v["postid"]: v for v in data}.values())
    with open(BOOKMARKS_PATH, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def remove_bookmark(BOOKMARKS_PATH, postid):
    data = read_json(BOOKMARKS_PATH)
    data = [bookmark for bookmark in data if bookmark["postid"] != postid]
    with open(BOOKMARKS_PATH, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def get_posts_by_bookmarks(data, BOOKMARKS_PATH):
    bookmarks = read_json(BOOKMARKS_PATH)
    results = []
    for bookmark in bookmarks:
        for post in data:
            if bookmark["postid"] == post["pk"]:
                results.append(post)
    return results
