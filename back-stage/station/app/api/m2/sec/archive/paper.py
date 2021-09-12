from flask import jsonify, request
from app.forms import PageForm, IdForm, SearchForm
from app.models import db, Paper, PaperAlbum
from app.schemas.sec.archive import PaperSchema, load_paper_with_check, CreatePaperSchema, UpdatePaperSchema, \
    dump_paper_with_check
from app.api.m2.sec import api
from bs4 import BeautifulSoup as bs4


@api.route('/archive/paper/<int:next_page>', methods=['GET'])
def get_paper(next_page):
    valid_form = PageForm(data={'page': next_page}).validate_for_api()
    paginate = Paper.query.with_entities(Paper.id, Paper.pf_name, Paper.pf_url, Paper.date, Paper.title, Paper.visible)\
        .paginate(page=valid_form['page'], per_page=20, error_out=False)
    paper_schema = PaperSchema()
    posts = paper_schema.dump(obj=paginate.items, many=True)
    return jsonify(data=posts, next_page=paginate.next_num), 200


@api.route('/archive/paper', methods=['PUT'])
def create_paper():
    paper = load_paper_with_check(CreatePaperSchema(exclude=['id']), request.get_json())
    from app.libs.upload import save_markdown_image
    paper.content = save_markdown_image(media_type='sec', content=paper.content)
    with db.auto_commit():
        db.session.add(paper)
    return jsonify(msg='done'), 201


@api.route('/archive/paper', methods=['PATCH'])
def update_paper():
    valid_schema = load_paper_with_check(UpdatePaperSchema(), request.get_json())
    base_query = Paper.query.filter_by(id=valid_schema['id'])
    query_paper = base_query.first_or_404()
    if 'albums' in valid_schema:
        albums = valid_schema.pop('albums')
        query_paper.albums.clear()
        for album in albums:
            post_album = PaperAlbum()
            post_album.name = album
            query_album = PaperAlbum.query.filter_by(name=album).first()
            if query_album:
                query_paper.albums.append(query_album)
            else:
                query_paper.albums.append(post_album)
    with db.auto_commit():
        base_query.update(valid_schema)
        return jsonify(msg='done'), 200


@api.route('/archive/paper/<int:paper_id>', methods=['DELETE'])
def delete_paper(paper_id):
    valid_form = IdForm(data={'id': paper_id}).validate_for_api()
    query_paper = Paper.query.get_or_404(valid_form['id'])
    with db.auto_commit():
        db.session.delete(query_paper)
        return jsonify(), 204


@api.route('/archive/paper/detail/<int:paper_id>', methods=['GET'])
def get_paper_detail(paper_id):
    valid_form = IdForm(data={'id': paper_id}).validate_for_api()
    query_paper = Paper.query.get_or_404(valid_form['id'])
    paper = PaperSchema().dump(query_paper)
    paper['albums'] = list(map(lambda x: x['name'], paper['albums']))
    return jsonify(data=paper), 200


@api.route('/archive/paper/search', methods=['POST'])
def search_paper():
    valid_form = SearchForm().validate_for_api()
    paginate = Paper.query.with_entities(Paper.id, Paper.pf_name, Paper.pf_url, Paper.date, Paper.visible, Paper.title)\
        .filter(Paper.title.like(f'%{valid_form["tracker"]}%'))\
        .paginate(page=valid_form['page'], per_page=1, error_out=False)
    papers = dump_paper_with_check(PaperSchema(many=True), paginate.items)
    return jsonify(data=papers, next_page=paginate.next_num), 200
