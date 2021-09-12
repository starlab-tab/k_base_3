from flask import jsonify
from sqlalchemy import or_
from app.api.v2.sec import api
from app.exceptions import Code404
from app.forms import PaperAlbumForm, PaperPfIdForm, PaperWithAlbumSearchForm, PaperSpellForm
from app.models import PaperAlbum, Paper, Paper_M_Album, db
from app.schemas.sec.archive import PaperAlbumSchema, PaperSchema


@api.route('/archive/paper/<string:pf_id>', methods=['GET'])
def get_archive_paper_detail(pf_id):
    valid_form = PaperPfIdForm(dict(pf_id=pf_id)).validate_for_api()
    query_paper = Paper.query.filter_by(pf_id=valid_form['pf_id']).first_or_404("No such paper")
    if not query_paper.visible:
        return jsonify(), 203
    blog = PaperSchema(many=False).dump(query_paper)
    blog['albums'] = list(map(lambda x: x['name'], blog['albums']))
    return jsonify(data=blog), 200


@api.route('/archive/paper/spell', methods=['POST'])
def verify_spell():
    valid_form = PaperSpellForm().validate_for_api()
    query_paper = Paper.query.filter_by(pf_id=valid_form['pf_id']).first_or_404("No such paper")
    if query_paper.protection == valid_form['spell']:
        paper = PaperSchema().dump(query_paper)
        paper['albums'] = list(map(lambda x: x['name'], paper['albums']))
        with db.auto_commit():
            return jsonify(data=paper), 200
    return Code404()


@api.route('/archive/album', methods=['GET'])
def get_archive_albums():
    albums = PaperAlbum.query.with_entities(PaperAlbum.id, PaperAlbum.name).all()
    schemas = PaperAlbumSchema(many=True)
    return jsonify(data=schemas.dump(albums)), 200


@api.route('/archive/album/<string:name>/<int:page>', methods=['GET'])
def get_archive_album_paper(name, page):
    valid_form = PaperAlbumForm(dict(name=name, page=page)).validate_for_api()
    if valid_form['name'].lower() == 'all':
        paginate = Paper.query\
            .with_entities(
                Paper.title, Paper.pf_id, Paper.pf_name, Paper.pf_url, Paper.author, Paper.visible, Paper.date
            )\
            .order_by(Paper.created_at.desc()) \
            .paginate(page=valid_form['page'], per_page=1, error_out=False)
    else:
        paginate = Paper.query.join(Paper_M_Album) \
            .join(PaperAlbum) \
            .with_entities(Paper.title, Paper.pf_id, Paper.pf_name, Paper.pf_url, Paper.author, Paper.visible, Paper.date) \
            .filter(PaperAlbum.name == valid_form['name']) \
            .order_by(Paper.created_at.desc()) \
            .paginate(page=valid_form['page'], per_page=1, error_out=False)
    papers = PaperSchema().dump(obj=paginate.items, many=True)
    return jsonify(data=papers, next_page=paginate.next_num), 200


@api.route('/archive/paper', methods=['POST'])
def search_archive_paper():
    valid_form = PaperWithAlbumSearchForm().validate_for_api()
    if valid_form['name'].lower() == 'all':
        paginate = Paper.query \
            .with_entities(
                Paper.title, Paper.pf_id, Paper.pf_name, Paper.pf_url, Paper.author, Paper.visible,Paper.date
            )\
            .filter(
                or_(Paper.title.like(f'%{valid_form["tracker"]}%'), Paper.author.like(f'%{valid_form["tracker"]}%'))
            )\
            .paginate(page=valid_form['page'], per_page=1, error_out=False)
    else:
        paginate = Paper.query.join(Paper_M_Album) \
            .join(PaperAlbum) \
            .with_entities(
                Paper.title, Paper.pf_id, Paper.pf_name, Paper.pf_url, Paper.author, Paper.visible, Paper.date
            )\
            .filter(
                PaperAlbum.name == valid_form['name'],
                or_(Paper.title.like(f'%{valid_form["tracker"]}%'), Paper.author.like(f'%{valid_form["tracker"]}%'))
            )\
            .order_by(Paper.created_at.desc()) \
            .paginate(page=valid_form['page'], per_page=1, error_out=False)
    papers = PaperSchema(many=True).dump(paginate.items)
    return jsonify(data=papers, next_page=paginate.next_num), 200
