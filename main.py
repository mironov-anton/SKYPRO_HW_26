from flask import Flask, render_template, request, send_from_directory, abort
from functions import read_json, posts_with_comments_count, get_comments_by_post, add_comment, get_posts_by_search

POSTS_PATH = "data/data.json"
COMMENTS_PATH = "data/comments.json"

app = Flask(__name__)


@app.route("/")
def page_feed():
    posts = posts_with_comments_count(POSTS_PATH, COMMENTS_PATH)
    return render_template('index.html', posts=posts)


@app.route("/post/<int:postid>/", methods=["GET", "POST"])
def page_post(postid):
    if request.method == 'GET':
        for post in read_json(POSTS_PATH):
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
    results = get_posts_by_search(posts_with_comments_count(POSTS_PATH, COMMENTS_PATH), s)
    if len(results) > 10:
        limited_results = results[:10]
    else:
        limited_results = results
    return render_template('search.html', results=limited_results, results_num=len(results))


if __name__ == "__main__":
    # os.chdir(Path(os.path.abspath(__file__)).parent)  # Эта строка необходима, чтобы правильно искать json хранилища
    app.run(debug=True)
