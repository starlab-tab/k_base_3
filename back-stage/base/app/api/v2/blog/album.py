from flask import jsonify
from app.forms import BlogAlbumPostForm, PageForm
from app.models import db, Blog, BlogAlbum, Blog_M_Album
from app.schemas.blog import BlogAlbumGroupSchema, BlogSchema
from app.api.v2.blog import api, SearchForm


@api.route('/album/<int:page_num>', methods=['GET'])
def get_blog_albums(page_num):
    valid_form = PageForm(data={'page': page_num}).validate_for_api()
    paginate = BlogAlbum.query.join(Blog_M_Album)\
        .join(Blog)\
        .group_by(BlogAlbum.id)\
        .with_entities(Blog.id.label("post_id"), Blog.title.label("post_title"), db.func.max(Blog.created_at).label("latest")
                       , BlogAlbum.name.label("album_name"), db.func.count(BlogAlbum.id).label("post_num"))\
        .paginate(page=valid_form['page'], per_page=24, error_out=False)
    album_group_schema = BlogAlbumGroupSchema()
    album_groups = album_group_schema.dump(obj=paginate.items, many=True)
    return jsonify(data=album_groups, total_pages=paginate.pages), 200


@api.route('/album/<string:album_name>/<int:page_num>', methods=['GET'])
def get_blog_album_post(album_name, page_num):
    valid_form = BlogAlbumPostForm(dict(name=album_name, page=page_num)).validate_for_api()
    paginate = Blog.query.join(Blog_M_Album) \
        .join(BlogAlbum) \
        .with_entities(Blog.id, Blog.title, Blog.views, Blog.visible, Blog.created_at) \
        .filter(BlogAlbum.name == valid_form['name'])\
        .order_by(Blog.created_at.desc())\
        .paginate(page=valid_form['page'], per_page=1, error_out=False)
    blog_schema = BlogSchema(only=['id', 'title', 'visible', 'views', 'created_at'])
    posts = blog_schema.dump(obj=paginate.items, many=True)
    return jsonify(data=posts, next_page=paginate.next_num), 200


@api.route('/album/search', methods=['POST'])
def search_blog_album():
    valid_form = SearchForm().validate_for_api()
    paginate = BlogAlbum.query.join(Blog_M_Album) \
        .join(Blog) \
        .with_entities(Blog.id.label("post_id"), Blog.title.label("post_title"),
                       db.func.max(Blog.created_at).label("latest")
                       , BlogAlbum.name.label("album_name"), db.func.count(BlogAlbum.id).label("post_num")) \
        .order_by(BlogAlbum.created_at.desc()) \
        .filter(BlogAlbum.name.like(f'%{valid_form["tracker"]}%'))\
        .group_by(BlogAlbum.id) \
        .paginate(page=valid_form['page'], per_page=24, error_out=False)
    album_group_schema = BlogAlbumGroupSchema()
    album_groups = album_group_schema.dump(obj=paginate.items, many=True)
    return jsonify(data=album_groups, total_pages=paginate.pages), 200