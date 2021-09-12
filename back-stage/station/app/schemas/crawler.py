from app.exceptions import Code400
from app.models import Crawler, ma, db
from marshmallow import post_load, fields, validate, ValidationError, validates_schema, Schema


class CrawlerSchema(ma.SQLAlchemyAutoSchema):
    id = fields.Integer(validate=[validate.Range(min=1, max=1000)], required=True)
    type = fields.Str(validate=[validate.Length(min=1, max=4), validate.OneOf(['json', 'html'])], required=True)
    platform = fields.Str(validate=[validate.Length(min=1, max=32)], required=True)
    base_url = fields.Str(validate=[validate.Length(min=1, max=64)], required=True)
    url_reg = fields.Str(validate=[validate.Length(min=1, max=128)], required=True)
    api = fields.Str(validate=[validate.Length(min=1, max=128)], required=True)
    custom = fields.Boolean(validate=[validate.OneOf([False, True])], required=True)
    pure_tags = fields.List(
        fields.Str(validate=validate.Length(min=1, max=16), required=False),
        validate=validate.Length(max=32), missing=list()
    )
    rules = fields.Dict(
        key=fields.Str(validate=[validate.Length(max=12), ], required=True),
        values=fields.List(
            fields.Str(validate=[validate.Length(min=1, max=256)], required=True),
            validate=[validate.Length(min=1, max=6)], required=True
        ),
        validate=[validate.Length(min=1, max=12)], required=True
    )

    @post_load
    def make_crawler(self, data, **kwargs):
        return Crawler(**data)


class CreateCrawlerSchema(CrawlerSchema):
    @validates_schema
    def validate_schema(self, data, **kwargs):
        if Crawler.query.with_entities(Crawler.id).filter(db.func.lower(Crawler.platform) == db.func.lower(data['platform'])).first():
            raise ValidationError('record exist', 'crawler')


class CreateJsonCrawlerSchema(CreateCrawlerSchema):
    pass


class CreateHtmlCrawlerSchema(CreateCrawlerSchema):
    rules = fields.Dict(
        key=fields.Str(validate=[validate.Length(max=12), ], required=True),
        values=fields.Str(validate=[validate.Length(min=1, max=256)], required=True),
        validate=[validate.Length(min=1, max=12)], required=True
    )


class UpdateCrawlerSchema(Schema):
    id = fields.Integer(validate=[validate.Range(min=1, max=1000)], required=True)
    platform = fields.Str(validate=[validate.Length(min=1, max=32)], required=False)
    base_url = fields.Str(validate=[validate.Length(min=1, max=64)], required=False)
    url_reg = fields.Str(validate=[validate.Length(min=1, max=128)], required=False)
    api = fields.Str(validate=[validate.Length(min=1, max=128)], required=False)
    type = fields.Str(validate=[validate.Length(min=1, max=4), validate.OneOf(['json', 'html'])], required=True)
    custom = fields.Boolean(validate=[validate.OneOf([False, True])], required=False)
    pure_tags = fields.List(
        fields.Str(validate=validate.Length(min=1, max=16), required=False),
        validate=validate.Length(max=32), required=False
    )
    rules = fields.Dict(
        key=fields.Str(validate=[validate.Length(max=12), ], required=True),
        values=fields.List(
            fields.Str(validate=[validate.Length(min=1, max=256)], required=True),
            validate=[validate.Length(min=1, max=6)], required=True
        ),
        validate=[validate.Length(min=1, max=12)], required=False
    )

    @validates_schema
    def validate_schema(self, data, **kwargs):
        Crawler.query.get_or_404(data['id'])


class UpdateJsonCrawlerSchema(UpdateCrawlerSchema):
    pass


class UpdateHtmlCrawlerSchema(UpdateCrawlerSchema):
    rules = fields.Dict(
        key=fields.Str(validate=[validate.Length(max=12), ], required=True),
        values=fields.Str(validate=[validate.Length(min=1, max=256)], required=True),
        validate=[validate.Length(min=1, max=12)], required=False
    )


def load_crawler_with_check(schema, data):
    try:
        return schema.load(data)
    except ValidationError as e:
        raise Code400(
            list(map(lambda x: ' | '.join(str(f'{x}: {text}') for text in e.messages[x]), e.messages))
        )


def dump_crawler_with_check(schema, data):
    try:
        return schema.dump(data)
    except ValidationError as e:
        raise Code400('crawler valid fail')