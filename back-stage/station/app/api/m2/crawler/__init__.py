from flask import request, jsonify

from app.exceptions import Code400, Code404
from app.forms import ActiveCrawlerForm, IdForm
from app.libs.m2print import M2print
from app.models import Crawler, db
from app.schemas.crawler import (
    load_crawler_with_check,
    dump_crawler_with_check, CreateJsonCrawlerSchema, CreateHtmlCrawlerSchema, UpdateJsonCrawlerSchema,
    UpdateHtmlCrawlerSchema
)
import importlib

api = M2print('crawler')


@api.route('', methods=['GET'])
def get_crawler():
    query_json_crawlers = Crawler.query.filter_by(type='json').all()
    query_html_crawlers = Crawler.query.filter_by(type='html').all()
    json_crawlers = dump_crawler_with_check(
        CreateJsonCrawlerSchema(many=True),
        query_json_crawlers
    )
    html_crawlers = dump_crawler_with_check(
        CreateHtmlCrawlerSchema(many=True),
        query_html_crawlers
    )
    json_crawlers.extend(html_crawlers)
    json_crawlers.sort(key=lambda x: x.get('id'))
    return jsonify(data=json_crawlers), 200


@api.route('', methods=['PUT'])
def create_crawler():
    crawler_type = request.get_json()['type']
    if crawler_type == 'json':
        crawler = load_crawler_with_check(CreateJsonCrawlerSchema(exclude=['id']), request.get_json())
    elif crawler_type == 'html':
        crawler = load_crawler_with_check(CreateHtmlCrawlerSchema(exclude=['id']), request.get_json())
    else:
        return Code400('crawler type invalid')
    try:
        db.session.add(crawler)
        db.session.commit()
        return jsonify(id=crawler.id), 201
    except Exception as e:
        print("rollback")
        db.session.rollback()
        raise e


@api.route('', methods=['PATCH'])
def update_crawler():
    crawler_type = request.get_json()['type']
    if crawler_type == 'json':
        valid_schema = load_crawler_with_check(UpdateJsonCrawlerSchema(), request.get_json())
    elif crawler_type == 'html':
        valid_schema = load_crawler_with_check(UpdateHtmlCrawlerSchema(), request.get_json())
    else:
        return Code400('crawler type invalid')
    base_query = Crawler.query.filter_by(id=valid_schema['id'])
    new_data = dict()
    for key in request.get_json():
        new_data[key] = valid_schema[key]
    with db.auto_commit():
        base_query.update(new_data)
        return jsonify(msg='done'), 200


@api.route('', methods=['POST'])
def active_crawler():
    valid_form = ActiveCrawlerForm().validate_for_api()
    crawler = Crawler.query.filter(db.func.lower(Crawler.platform) == db.func.lower(valid_form['platform'])).first_or_404()
    if crawler.custom:
        module = importlib.import_module(f'app.utils.crawler.{valid_form["platform"]}')
        analyst = module.Analyst(pf_id=valid_form["id"], part_url=valid_form['part_url'], crawler=crawler)
    else:
        if crawler.type == 'json':
            from app.utils.crawler.json_analyst import JsonAnalyst
            analyst = JsonAnalyst(pf_id=valid_form["id"], part_url=valid_form['part_url'], crawler=crawler)
        elif crawler.type == 'html':
            from app.utils.crawler.html_analyst import HtmlAnalyst
            analyst = HtmlAnalyst(pf_id=valid_form["id"], part_url=valid_form['part_url'], crawler=crawler)
        else:
            raise Code404('wrong crawler type')
    analyst.fetch_with_get()
    return jsonify(data=analyst.dump_data), 201
    

@api.route('/<int:crawler_id>', methods=['DELETE'])
def delete_crawler(crawler_id):
    valid_form = IdForm(data={'id': crawler_id}).validate_for_api()
    query_crawler = Crawler.query.get_or_404(valid_form['id'])
    with db.auto_commit():
        db.session.delete(query_crawler)
        return jsonify(), 204
