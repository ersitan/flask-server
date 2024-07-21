import sqlite3
from flask import Flask, request, jsonify, render_template
from werkzeug.exceptions import abort
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)


#
# basedir = os.path.abspath(os.path.dirname(__file__))
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')
# db = SQLAlchemy(app)
# ma = Marshmallow(app)
#
#
# class Guide(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(100), unique=False)
#     content = db.Column(db.String(144), unique=False)
#
#     def __init__(self, title, content):
#         self.title = title
#         self.content = content
#
#
# class GuideSchema(ma.Schema):
#     class Meta:
#         fields = ('title', 'content')
#
#
# guide_schema = GuideSchema()
# guides_schema = GuideSchema(many=True)
#

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post

@app.route('/')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)

@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)


#
#
# # Endpoint to create a new guide
# @app.post('/guide')
# def add_guide():
#     title = request.json['title']
#     content = request.json['content']
#
#     new_guide = Guide(title, content)
#
#     db.session.add(new_guide)
#     db.session.commit()
#
#     guide = db.session.get(Guide, new_guide.id)
#
#     return guide_schema.jsonify(guide)
#
#
# @app.get('/guide')
# def get_guides():
#     all_guides = Guide.query.all()
#     result = guides_schema.dump(all_guides)
#     return jsonify(result)
#
#
# @app.get('/guide/<int:id>')
# def get_guide(id):
#     guide = db.session.get(Guide, id)
#     result = guide_schema.dump(guide)
#     return jsonify(result)
#
#
# # Endpoint for updating a guide
# @app.put("/guide/<int:id>")
# def guide_update(id):
#     guide = db.session.get(Guide, id)
#     title = request.json['title']
#     content = request.json['content']
#
#     guide.title = title
#     guide.content = content
#
#     db.session.commit()
#     return guide_schema.jsonify(guide)
#

if __name__ == '__main__':
    app.run(host="localhost", debug=True)
