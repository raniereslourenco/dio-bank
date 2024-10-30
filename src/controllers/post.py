from flask import Blueprint, request
from sqlalchemy import inspect
from src.app import User, Post, db
from http import HTTPMethod, HTTPStatus

app = Blueprint('post', __name__, url_prefix="/posts")

def _create_post():
    data = request.json
    post = Post(title=data["title"], body=data["body"], author_id=data["author_id"])
    db.session.add(post)
    db.session.commit()

def _list_posts():
    query = db.select(Post)
    posts = db.session.execute(query).scalars()
    return [
        {'id': post.id, 'Title': post.title, 'Body': post.body, 'Author': post.author_id, 'Created at': post.created, }
        for post in posts
    ]

@app.route('/', methods=['GET', 'POST'])
def handle_user():
    if request.method == 'POST':
       _create_post()
       return {'message': "Post created"}, HTTPStatus.CREATED
    else:
        return {'posts': _list_posts()}
    
@app.route('/<int:post_id>')
def get_post(post_id):
    posts = db.get_or_404(Post, post_id)
    # user = db.get_or_404(User, use)
    return
    {
        'id': posts.id, 
        'Title': posts.title,
        'Body': posts.body,
        'Created at': posts.created,
    }

@app.route('/<int:post_id>', methods=['PATCH'])
def update_post(post_id):
    post = db.get_or_404(Post, post_id)
    data = request.json

    mapper = inspect(Post)
    for column in mapper.attrs:
        if column.key in data:
            setattr(post, column.key, data[column.key])
    db.session.commit()

    return [
        {
            'id': post.id, 
            'Title': post.title,
            'Body': post.body,
            'Author': post.author_id,
            'Created at': post.created,
        }
    ]

@app.route('/<int:post_id>', methods=["DELETE"])
def delete_post(post_id):
    post = db.get_or_404(Post, post_id)
    db.session.delete(post)
    db.session.commit()
    return "", HTTPStatus.NO_CONTENT