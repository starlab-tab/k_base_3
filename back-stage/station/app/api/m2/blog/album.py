from flask import jsonify
from app.exceptions import Code404
from app.forms import UpdateAlbumForm, PageForm, SearchForm, IdForm
from app.models import db, BlogAlbum
from app.schemas.blog import BlogAlbumSchema
from app.api.m2.blog import api


@api.route('/album/<int:next_page>', methods=['GET'])
def get_blog_albums(next_page):
    valid_form = PageForm(data={'page': next_page}).validate_for_api()
    if valid_form['page'] == 0:
        albums = BlogAlbum.query.with_entities(BlogAlbum.name).all()
        return jsonify(data=albums), 200
    else:
        paginate = BlogAlbum.query.paginate(page=valid_form['page'], per_page=10, error_out=False)
        blog_schema = BlogAlbumSchema(only=['id', 'name', 'nums'])
        albums = blog_schema.dump(obj=paginate.items, many=True)
        return jsonify(data=albums,next_page=paginate.next_num), 200


@api.route('/album', methods=['PATCH'])
def update_blog_album():
    valid_form = UpdateAlbumForm().validate_for_api()
    query_album = BlogAlbum.query.get_or_404(valid_form['id'])
    if BlogAlbum.query.filter(db.func.lower(BlogAlbum.name) == db.func.lower(valid_form['album_name'])).first():
        return Code404("record exist")
    with db.auto_commit():
        query_album.name = valid_form['album_name']
        return jsonify(), 200


@api.route('/album/search', methods=['POST'])
def search_blog_album():
    valid_form = SearchForm().validate_for_api()
    paginate = BlogAlbum.query.filter(BlogAlbum.name.like(f'%{valid_form["tracker"]}%'))\
        .paginate(page=valid_form['page'], per_page=20, error_out=False)
    blog_schema = BlogAlbumSchema(only=['id', 'name', 'nums'])
    albums = blog_schema.dump(obj=paginate.items, many=True)
    return jsonify(data=albums, next_page=paginate.next_num), 200


@api.route('/album/<int:album_id>', methods=['DELETE'])
def delete_blog_album(album_id):
    valid_form = IdForm(data={'id': album_id}).validate_for_api()
    query_album = BlogAlbum.query.get_or_404(valid_form['id'])
    with db.auto_commit():
        db.session.delete(query_album)
        return jsonify(), 204
