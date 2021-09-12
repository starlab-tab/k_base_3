from flask import jsonify
from app.api.m2.sec import api
from app.exceptions import Code404
from app.forms import PageForm, UpdateAlbumForm, IdForm, SearchForm
from app.models import PaperAlbum, db, Paper
from app.schemas.sec.archive import PaperAlbumSchema, PaperSchema


@api.route('/archive/album/<int:next_page>', methods=['GET'])
def get_paper_albums(next_page):
    valid_form = PageForm(data={'page': next_page}).validate_for_api()
    if valid_form['page'] == 0:
        albums = PaperAlbum.query.with_entities(PaperAlbum.name).all()
        return jsonify(data=albums), 200
    else:
        paginate = PaperAlbum.query.paginate(page=valid_form['page'], per_page=20, error_out=False)
        paper_schema = PaperAlbumSchema(only=['id', 'name', 'nums'])
        albums = paper_schema.dump(obj=paginate.items, many=True)
        return jsonify(data=albums, next_page=paginate.next_num), 200


@api.route('/archive/album', methods=['PATCH'])
def update_paper_album():
    valid_form = UpdateAlbumForm().validate_for_api()
    query_album = PaperAlbum.query.get_or_404(valid_form['id'])
    if PaperAlbum.query.filter_by(db.func.lower(PaperAlbum.name) == db.func.lower(valid_form['album_name'])).first():
        return Code404("record exist")
    with db.auto_commit():
        query_album.name = valid_form['album_name']
        return jsonify(), 200



@api.route('/archive/album/search', methods=['POST'])
def search_paper_album():
    valid_form = SearchForm().validate_for_api()
    paginate = PaperAlbum.query.filter(PaperAlbum.name.like(f'%{valid_form["tracker"]}%'))\
        .paginate(page=valid_form['page'], per_page=20, error_out=False)
    paper_schema = PaperAlbumSchema(only=['id', 'name', 'nums'])
    albums = paper_schema.dump(obj=paginate.items, many=True)
    return jsonify(data=albums, next_page=paginate.next_num), 200


@api.route('/archive/album/<int:paper_id>', methods=['DELETE'])
def delete_paper_album(paper_id):
    valid_form = IdForm(data={'id': paper_id}).validate_for_api()
    query_album = PaperAlbum.query.get_or_404(valid_form['id'])
    with db.auto_commit():
        db.session.delete(query_album)
        return jsonify(), 204



