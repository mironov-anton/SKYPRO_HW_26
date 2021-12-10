from functions import read_json, get_comments_by_post
from collections import Counter

POSTS_PATH = "data/data.json"
COMMENTS_PATH = "data/comments.json"
comments = read_json(COMMENTS_PATH)
# comments_p =
comments_num = dict(Counter([x['post_id'] for x in comments]))

posts = read_json(POSTS_PATH)
for post in posts:
    for key in comments_num:
        if post["pk"] == key:
            post["comments_count"] = comments_num[key]
    if "comments_count" not in post:
        post["comments_count"] = 0

comments = get_comments_by_post(COMMENTS_PATH, 7)
print(comments)
