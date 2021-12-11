from flask import Flask, render_template, request, abort, redirect
from functions import read_json, posts_with_comments_count, get_comments_by_post, add_comment, get_posts_by_search, \
    get_posts_by_username, tags_to_links, get_posts_by_tag, add_bookmark, remove_bookmark

POSTS_PATH = "data/data.json"
COMMENTS_PATH = "data/comments.json"
BOOKMARKS_PATH = "data/bookmarks.json"

app = Flask(__name__)


@app.errorhandler(404)
def page_not_found(e):
    return "Страница не найдена. Подумайте, нужна ли она вам. Если да - попробуйте ещё раз, но честно говоря, " \
           "вряд ли что-то изменится.", 404


@app.route("/")
def page_feed():
    posts = tags_to_links(posts_with_comments_count(POSTS_PATH, COMMENTS_PATH))
    return render_template('index.html', posts=posts)


@app.route("/post/<int:postid>/", methods=["GET", "POST"])
def page_post(postid):
    if request.method == 'GET':
        for post in tags_to_links(read_json(POSTS_PATH)):
            if postid == post["pk"]:
                comments = get_comments_by_post(COMMENTS_PATH, postid)
                return render_template('post.html', **post, comments=comments, comments_num=len(comments))
        abort(404)
    commenter_name = request.form.get('commenter_name')
    comment_text = request.form.get('comment')
    comment = {
        "post_id": postid,
        "commenter_name": commenter_name,
        "comment": comment_text,
        "pk": len(read_json(COMMENTS_PATH)) + 1
    }
    add_comment(COMMENTS_PATH, comment)
    for post in read_json(POSTS_PATH):
        if postid == post["pk"]:
            comments = get_comments_by_post(COMMENTS_PATH, postid)
            return render_template('post.html', **post, comments=comments, comments_num=len(comments))


@app.route("/search/")
def page_search():
    s = request.args.get('s')
    if not s:
        return render_template('search.html', results_num=0)
    results = tags_to_links(get_posts_by_search(posts_with_comments_count(POSTS_PATH, COMMENTS_PATH), s))
    if len(results) > 10:
        limited_results = results[:10]
    else:
        limited_results = results
    return render_template('search.html', results=limited_results, results_num=len(results))


@app.route("/users/<username>/")
def page_user(username):
    user_posts = tags_to_links(get_posts_by_username(posts_with_comments_count(POSTS_PATH, COMMENTS_PATH), username))
    return render_template("user-feed.html", user_posts=user_posts)


@app.route("/tag/<tagname>/")
def page_tag(tagname):
    tag_posts = tags_to_links(get_posts_by_tag(posts_with_comments_count(POSTS_PATH, COMMENTS_PATH), tagname))
    return render_template("tag.html", tag_posts=tag_posts)


@app.route("/bookmarks/add/<int:postid>/")
def adding_bookmark(postid):
    add_bookmark(BOOKMARKS_PATH, postid)
    return redirect("/", code=302)


@app.route("/bookmarks/remove/<int:postid>/")
def removing_bookmark(postid):
    remove_bookmark(BOOKMARKS_PATH, postid)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
