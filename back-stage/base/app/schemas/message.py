from marshmallow import validate, fields, ValidationError, post_load

from app.exceptions import Code400
from app.models import ma, Message


class MessageSchema(ma.SQLAlchemyAutoSchema):
    texter = fields.Str(validate=[validate.Length(min=1, max=36)], required=True)
    text = fields.Str(validate=[validate.Length(min=1, max=360)], required=True)

    class Meta:
        model = Message

    @post_load
    def make_message(self, data, **kwargs):
        message = Message(**data)
        return message


def load_message_with_check(schema, data):
    try:
        return schema.load(data)
    except ValidationError as e:
        raise Code400('message valid fail')