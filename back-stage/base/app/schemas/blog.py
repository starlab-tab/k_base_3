from app.models import Blog, ma, BlogAlbum


class BlogAlbumSchema(ma.SQLAlchemyAutoSchema):
    blogs = ma.Function(lambda obj: len(obj.blogs))

    class Meta:
        model = BlogAlbum


class BlogSchema(ma.SQLAlchemyAutoSchema):
    albums = ma.Nested(BlogAlbumSchema, many=True, only=['name'])
    chips = ma.Function(lambda obj: obj.chips if obj.chips else list())

    class Meta:
        model = Blog


class BlogAlbumGroupSchema(ma.Schema):
    class Meta:
        fields = ('post_id', 'post_title', 'latest', 'album_name', 'post_num')