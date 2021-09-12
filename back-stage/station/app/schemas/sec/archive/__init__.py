from marshmallow import post_load, fields, validate, validates_schema, ValidationError

from app.exceptions import Code400
from app.models import ma, Paper, PaperAlbum, db


class PaperAlbumSchema(ma.SQLAlchemyAutoSchema):
    nums = ma.Function(lambda obj: len(obj.papers))

    class Meta:
        model = PaperAlbum


def check_visible(data):
    if 'visible' in data and not data['visible']:
        if 'protection' not in data:
            raise Code400('missing protection')
        else:
            if len(data['protection']) <= 0:
                raise Code400('protection iv len')
    else:
        data.pop('protection', None)


class PaperSchema(ma.SQLAlchemyAutoSchema):
    id = fields.Integer(validate=[validate.Range(min=1, max=1000, error="invalid")], required=True)
    pf_id = fields.Str(validate=[validate.Length(min=1, max=36, error="iv len")], required=True)
    pf_name = fields.Str(validate=[validate.Length(min=1, max=16, error="iv len")], required=True)
    pf_url = fields.Str(validate=[validate.Length(min=1, max=128, error="iv len")], required=True)
    author = fields.Str(validate=[validate.Length(min=1, max=32, error="iv len")], required=True)
    date = fields.Str(validate=[validate.Length(max=32, error="iv len")], required=False)
    title = fields.Str(validate=[validate.Length(min=1, max=128, error="iv len")], required=True)
    content = fields.Str(validate=[validate.Length(max=199800, error="iv len")], required=True)
    visible = fields.Boolean(validate=[validate.OneOf([False, True], error="iv type")], required=True)
    protection = fields.Str(validate=[validate.Length(max=12, error="iv len")], required=False)
    render = fields.Boolean(validate=[validate.OneOf([False, True], error="iv type")], required=False)
    chips = fields.List(
        fields.Str(validate=validate.Length(min=1, max=30, error="iv len"), required=False),
        validate=validate.Length(max=10, error="iv len"), required=False, missing=list()
    )
    albums = ma.Nested(PaperAlbumSchema, many=True, only=['name'], required=False)

    class Meta:
        model = Paper

    @validates_schema
    def validate_schema(self, data, **kwargs):
        if Paper.query.with_entities(Paper.id).filter(db.func.lower(Paper.pf_id) == db.func.lower(data['pf_id'])).first():
            raise ValidationError('record exist', 'paper')
        check_visible(data)

    @post_load
    def make_paper(self, data, **kwargs):
        return Paper(**data)


class CreatePaperSchema(PaperSchema):
    albums = fields.List(
        fields.Str(validate=validate.Length(min=1, max=30), required=False),
        validate=validate.Length(max=5), missing=list()
    )

    @post_load
    def make_paper(self, data, **kwargs):
        albums = data.pop('albums', list())
        paper = Paper(**data)
        for name in albums:
            new_album = PaperAlbum()
            new_album.name = name
            query_album = PaperAlbum.query.filter(db.func.lower(PaperAlbum.name) == db.func.lower(name)).first()
            if query_album:
                paper.albums.append(query_album)
            else:
                paper.albums.append(new_album)
        return paper


class UpdatePaperSchema(PaperSchema):
    pf_id = fields.Str(validate=[validate.Length(min=1, max=36, error="iv len")], required=False)
    pf_name = fields.Str(validate=[validate.Length(min=1, max=16, error="iv len")], required=False)
    pf_url = fields.Str(validate=[validate.Length(min=1, max=128, error="iv len")], required=False)
    author = fields.Str(validate=[validate.Length(min=1, max=32, error="iv len")], required=False)
    title = fields.Str(validate=[validate.Length(min=1, max=128, error="iv len")], required=False)
    content = fields.Str(validate=[validate.Length(max=199800, error="iv len")], required=False)
    visible = fields.Boolean(validate=[validate.OneOf([False, True], error="iv type")], required=False)
    chips = fields.List(
        fields.Str(validate=validate.Length(min=1, max=30, error="iv len"), required=False),
        validate=validate.Length(max=10, error="iv len"), required=False
    )
    albums = fields.List(
        fields.Str(validate=validate.Length(min=1, max=30, error="iv len"), required=False),
        validate=validate.Length(max=5, error="iv len"), required=False
    )

    @validates_schema
    def validate_schema(self, data, **kwargs):
        check_visible(data)

    @post_load
    def make_paper(self, data, **kwargs):
        return data


def load_paper_with_check(schema, data):
    try:
        return schema.load(data)
    except ValidationError as e:
        # raise Code400('paper valid fail')
        raise Code400(
            list(map(lambda x: ' | '.join(str(f'{x}: {text}') for text in e.messages[x]), e.messages))
        )


def dump_paper_with_check(schema, data):
    try:
        return schema.dump(data)
    except ValidationError as e:
        raise Code400('paper valid fail')
