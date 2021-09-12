from flask import request, jsonify
from app.forms import SearchForm, PageForm, IdForm
from app.models import db, Blog, BlogAlbum
from app.schemas.blog import BlogSchema, load_blog_with_check, CreateBlogSchema, UpdateBlogSchema
from app.api.m2.blog import api
from bs4 import BeautifulSoup as bs4
import markdown


@api.route('/post/<int:next_page>', methods=['GET'])
def get_blog_post(next_page):
    valid_form = PageForm(data={'page': next_page}).validate_for_api()
    paginate = Blog.query.with_entities(Blog.id, Blog.title, Blog.visible, Blog.views) \
        .paginate(page=valid_form['page'], per_page=20, error_out=False)
    blog_schema = BlogSchema(only=('id', 'title', 'visible', 'views'))
    posts = blog_schema.dump(obj=paginate.items, many=True)
    return jsonify(data=posts, next_page=paginate.next_num), 200


@api.route('/post', methods=['PUT'])
def create_blog_post():
    blog = load_blog_with_check(CreateBlogSchema(exclude=['id']), request.get_json())
    if len(blog.content) > 0:
        soup = bs4(markdown.markdown(blog.content[:1600]), "lxml")
        blog.desc = soup.text[0:170]
    with db.auto_commit():
        db.session.add(blog)
    return jsonify(msg='done'), 201


@api.route('/post', methods=['PATCH'])
def update_blog_post():
    valid_schema = load_blog_with_check(UpdateBlogSchema(), request.get_json())
    base_query = Blog.query.filter_by(id=valid_schema['id'])
    query_post = base_query.first_or_404()
    if 'albums' in valid_schema:
        albums = valid_schema.pop('albums')
        query_post.albums.clear()
        for album in albums:
            post_album = BlogAlbum()
            post_album.name = album
            query_album = BlogAlbum.query.filter_by(name=album).first()
            if query_album:
                query_post.albums.append(query_album)
            else:
                query_post.albums.append(post_album)
    if 'content' in valid_schema:
        soup = bs4(valid_schema['content'], "lxml")
        if query_post.desc != soup.text[:170]:
            query_post.desc = soup.text[:170]
    with db.auto_commit():
        base_query.update(valid_schema)
        return jsonify(msg='done'), 200


@api.route('/post/<int:post_id>', methods=['DELETE'])
def delete_blog_post(post_id):
    valid_form = IdForm(data={'id': post_id}).validate_for_api()
    query_blog = Blog.query.get_or_404(valid_form['id'])
    with db.auto_commit():
        db.session.delete(query_blog)
        return jsonify(), 204


@api.route('/post/detail/<int:post_id>', methods=['GET'])
def get_blog_post_detail(post_id):
    valid_form = IdForm(data={'id': post_id}).validate_for_api()
    query_blog = Blog.query.get_or_404(valid_form['id'])
    blog_schema = BlogSchema()
    post = blog_schema.dump(query_blog)
    post['albums'] = list(map(lambda x: x['name'], post['albums']))
    return jsonify(data=post), 200


@api.route('/post/search', methods=['POST'])
def search_blog_post():
    valid_form = SearchForm().validate_for_api()
    paginate = Blog.query.filter(Blog.title.like(f'%{valid_form["tracker"]}%'))\
        .paginate(page=valid_form['page'], per_page=1, error_out=False)
    posts = BlogSchema(only=('id', 'title', 'visible')).dump(obj=paginate.items, many=True)
    return jsonify(data=posts, next_page=paginate.next_num), 200
