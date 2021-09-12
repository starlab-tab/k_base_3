from flask import jsonify, request
from app.forms import PageForm, IdForm
from app.libs.m2print import M2print
from app.models import db, Message
from app.schemas.message import load_message_with_check, MessageSchema, EditMessageSchema

api = M2print('message')


@api.route('/<int:page_num>', methods=['GET'])
def get_messages(page_num):
    valid_form = PageForm(data={'page': page_num}).validate_for_api()
    paginate = Message.query.order_by(Message.created_at.desc()).paginate(page=valid_form['page'], per_page=50, error_out=False)
    messages = MessageSchema().dump(obj=paginate.items, many=True)
    return jsonify(data=messages, next_page=paginate.next_num), 200


@api.route('', methods=['POST'])
def create_message():
    message = load_message_with_check(MessageSchema(exclude=('id', 'supervisor', 'created_at', 'updated_at', 'ip')), request.get_json())
    try:
        db.session.add(message)
        db.session.commit()
        return jsonify(id=message.id), 201
    except Exception as e:
        print("rollback")
        db.session.rollback()
        raise e


@api.route('', methods=['PATCH'])
def edit_message():
    valid_schema = load_message_with_check(EditMessageSchema(exclude=('marked', 'created_at', 'updated_at', 'ip')), request.get_json())
    base_query = Message.query.filter_by(id=valid_schema['id'])
    message = base_query.first_or_404("No such message")
    if message.marked:  valid_schema.pop('supervisor', None)
    with db.auto_commit():
        base_query.update(valid_schema)
        return jsonify(msg='done'), 201


@api.route('/<int:message_id>', methods=['DELETE'])
def delete_message(message_id):
    valid_form = IdForm(data={'id': message_id}).validate_for_api()
    query_blog = Message.query.get_or_404(valid_form['id'], "No such message")
    with db.auto_commit():
        db.session.delete(query_blog)
        return jsonify(), 204
