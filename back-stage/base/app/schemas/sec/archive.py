from app.models import ma, Paper, PaperAlbum


class PaperAlbumSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PaperAlbum


class PaperSchema(ma.SQLAlchemyAutoSchema):
    albums = ma.Nested(PaperAlbumSchema, many=True, only=['name'])
    date = ma.Function(lambda obj: obj.date if len(obj.date) else 'no date')

    class Meta:
        model = Paper
