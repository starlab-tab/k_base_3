from app.exceptions import Code400
from app.models import Blog, ma, BlogAlbum, db
from marshmallow import post_load, fields, validate, ValidationError, Schema, validates_schema


class BlogAlbumSchema(ma.SQLAlchemyAutoSchema):
    nums = ma.Function(lambda obj: len(obj.blogs))

    class Meta:
        model = BlogAlbum


class BlogSchema(ma.SQLAlchemyAutoSchema):
    id = fields.Integer(validate=[validate.Range(min=1, max=1000)], required=True)
    title = fields.Str(validate=[validate.Length(min=1, max=130)], required=True)
    cover = fields.Str(validate=[validate.Length(max=120)], required=True)
    maker = fields.Str(validate=[validate.Length(max=20)], missing="no one")
    visible = fields.Boolean(validate=[validate.OneOf([False, True])], required=True)
    protection = fields.Str(validate=[validate.Length(max=12)], required=False)
    content = fields.Str(validate=[validate.Length(max=199800)], required=True)
    chips = fields.List(
        fields.Str(validate=validate.Length(min=1, max=30), required=False),
        validate=validate.Length(max=10), required=False
    )
    albums = ma.Nested(BlogAlbumSchema, many=True, only=['name'], required=False)

    class Meta:
        model = Blog


    @validates_schema
    def validate_schema(self, data, **kwargs):
        if 'visible' in data and not data['visible']:
            if 'protection' not in data:
                raise Code400('missing protection')
            else:
                if len(data['protection']) <= 0:
                    raise Code400('missing protection')
        else:
            data.pop('protection', None)


class CreateBlogSchema(BlogSchema):
    albums = fields.List(
        fields.Str(validate=validate.Length(min=1, max=30), required=False),
        validate=validate.Length(max=5), missing=list()
    )

    @post_load
    def make_blog(self, data, **kwargs):
        albums = data.pop('albums', list())
        blog = Blog(**data)
        for name in albums:
            new_album = BlogAlbum()
            new_album.name = name
            query_album = BlogAlbum.query.filter(db.func.lower(BlogAlbum.name) == db.func.lower(name)).first()
            if query_album:
                blog.albums.append(query_album)
            else:
                blog.albums.append(new_album)
        return blog


class UpdateBlogSchema(BlogSchema):
    title = fields.Str(validate=[validate.Length(min=1, max=120)], required=False)
    cover = fields.Str(validate=[validate.Length(max=110)], required=False)
    maker = fields.Str(validate=[validate.Length(max=20)], required=False)
    visible = fields.Boolean(validate=[validate.OneOf([False, True])], required=False)
    protection = fields.Str(validate=[validate.Length(min=1, max=12)], required=False)
    content = fields.Str(validate=[validate.Length(max=199800)], required=False)
    chips = fields.List(
        fields.Str(validate=validate.Length(min=1, max=30), required=False),
        validate=validate.Length(max=10), required=False
    )
    albums = fields.List(
        fields.Str(validate=validate.Length(min=1, max=30), required=False),
        validate=validate.Length(max=5), required=False
    )

    @post_load
    def make_blog(self, data, **kwargs):
        return data

    @validates_schema
    def validate_schema(self, data, **kwargs):
        if 'visible' in data and not data['visible']:
            if 'protection' not in data:
                raise Code400('missing protection')
        else:
            data.pop('protection', None)


def load_blog_with_check(schema, data):
    try:
        return schema.load(data)
    except ValidationError as e:
        raise Code400(
            list(map(lambda x: ' | '.join(str(f'{x}: {text}') for text in e.messages[x]), e.messages))
        )


def dump_blog_with_check(schema, data):
    try:
        return schema.dump(data)
    except ValidationError as e:
        raise Code400('blog valid fail')
