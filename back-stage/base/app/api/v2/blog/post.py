from flask import jsonify

from app.exceptions import Code404
from app.forms import SearchForm, PageForm, IdForm, BlogSpellForm
from app.models import db, Blog
from app.schemas.blog import BlogSchema
from app.api.v2.blog import api


@api.route('/post/<int:page_num>', methods=['GET'])
def get_blog_posts(page_num):
    valid_form = PageForm(data={'page': page_num}).validate_for_api()
    paginate = Blog.query.order_by(Blog.created_at.desc()).paginate(page=valid_form['page'], per_page=20, error_out=False)
    blog_schema = BlogSchema(only=('id', 'title', 'visible', 'created_at', 'albums', 'chips', 'desc', 'views'))
    posts = blog_schema.dump(obj=paginate.items, many=True)
    return jsonify(data=posts, total_pages=paginate.pages), 200


@api.route('/post/detail/<int:post_id>', methods=['GET'])
def get_blog_post_detail(post_id):
    valid_form = IdForm(data={'id': post_id}).validate_for_api()
    query_blog = Blog.query.get_or_404(valid_form['id'], "No such blog")
    if not query_blog.visible:
        return jsonify(), 203
    blog = BlogSchema(many=False).dump(query_blog)
    blog['albums'] = list(map(lambda x: x['name'], blog['albums']))
    with db.auto_commit():
        query_blog.views = query_blog.views + 1
        return jsonify(data=blog), 200


@api.route('/post/detail', methods=['POST'])
def verify_spell():
    valid_form = BlogSpellForm().validate_for_api()
    query_blog = Blog.query.get_or_404(valid_form['id'], "No such blog")
    if query_blog.protection == valid_form['spell']:
        blog = BlogSchema().dump(query_blog)
        blog['albums'] = list(map(lambda x: x['name'], blog['albums']))
        with db.auto_commit():
            query_blog.views = query_blog.views + 1
            return jsonify(data=blog), 200
    return Code404()


@api.route('/post/search', methods=['POST'])
def search_blog_post():
    valid_form = SearchForm().validate_for_api()
    paginate = Blog.query\
        .with_entities(Blog.id, Blog.title, Blog.visible, Blog.created_at, Blog.chips, Blog.desc, Blog.albums)\
        .filter(Blog.title.like(f'%{valid_form["tracker"]}%')) \
        .paginate(page=valid_form['page'], per_page=1, error_out=False)
    blog_schema = BlogSchema()
    posts = blog_schema.dump(obj=paginate.items, many=True)
    return jsonify(data=posts, total_pages=paginate.pages), 200
