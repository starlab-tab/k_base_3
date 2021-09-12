from marshmallow import validate, fields, ValidationError, post_load
from app.exceptions import Code400
from app.models import ma, Message


class MessageSchema(ma.SQLAlchemyAutoSchema):
    id = fields.Integer(validate=[validate.Range(min=1, max=10000)], required=True)
    texter = fields.Str(validate=[validate.Length(min=1, max=36)], required=True)
    text = fields.Str(validate=[validate.Length(min=1, max=360)], required=True)
    supervisor = fields.Str(validate=[validate.Length(max=360)], required=False)
    marked = fields.Boolean(validate=[validate.OneOf([False, True])], required=False)

    class Meta:
        model = Message

    @post_load
    def make_message(self, data, **kwargs):
        message = Message(**data)
        return message


class EditMessageSchema(MessageSchema):

    @post_load
    def make_message(self, data, **kwargs):
        return data


def load_message_with_check(schema, data):
    try:
        return schema.load(data)
    except ValidationError as e:
        raise Code400(
            list(map(lambda x: ' | '.join(str(f'{x}: {text}') for text in e.messages[x]), e.messages))
        )