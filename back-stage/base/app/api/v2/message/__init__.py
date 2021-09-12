from flask import jsonify, request
from app.forms import PageForm
from app.libs.v2print import V2print
from app.models import db, Message
from app.schemas.message import load_message_with_check, MessageSchema

api = V2print('message')


@api.route('/<int:page_num>', methods=['GET'])
def get_messages(page_num):
    valid_form = PageForm(data={'page': page_num}).validate_for_api()
    paginate = Message.query.order_by(Message.created_at.desc())\
        .paginate(page=valid_form['page'], per_page=50, error_out=False)
    messages = MessageSchema(exclude=('id','ip')).dump(obj=paginate.items, many=True)
    return jsonify(data=messages, next_page=paginate.next_num), 200


@api.route('', methods=['POST'])
def create_message():
    message = load_message_with_check(MessageSchema(
        exclude=('id', 'created_at', 'updated_at', 'supervisor', 'marked', 'ip')
    ), request.get_json())
    query_message = Message.query.filter(db.func.lower(Message.text) == db.func.lower(message.text)).first()
    if query_message:
        return jsonify(msg='done'), 201
    # message.ip = request.remote_addr
    ip = request.headers.get('X-Real-Ip', "wrong code")
    with db.auto_commit():
        db.session.add(message)
        return jsonify(msg='done'), 201
