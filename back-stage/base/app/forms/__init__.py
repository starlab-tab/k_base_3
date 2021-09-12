from flask import request
from wtforms import Form, IntegerField, StringField
from wtforms.validators import DataRequired, NumberRange, Length, ValidationError, NoneOf

from app.exceptions import Code404
from app.models import Blog, PaperAlbum, BlogAlbum


class BaseForm(Form):
    def __init__(self, data=None):
        if not data:
            data = request.get_json(silent=True)
        super(BaseForm, self).__init__(data=data)

    def validate_for_api(self):
        valid = super(BaseForm, self).validate()
        if not valid:
            # raise Code404(msg=self.errors)
            # raise Code404(msg=list(map(lambda x: ' | '.join(str(f'{x}: {text}') for text in self.errors[x]), self.errors)))
            raise Code404(msg='try harder...')
        return self.data


class IdForm(BaseForm):
    id = IntegerField(validators=[DataRequired('missing id'), NumberRange(1, 1000, 'id invalid')])


class PageForm(BaseForm):
    page = IntegerField(validators=[NumberRange(0, 1000, 'page num invalid')])


class SearchForm(PageForm):
    tracker = StringField(validators=[DataRequired('tracker invalid'), Length(1, 32, 'tracker invalid')])


class PaperWithAlbumSearchForm(SearchForm):
    name = StringField(validators=[DataRequired('name invalid'), Length(1, 32, 'name invalid')])



class BlogSpellForm(IdForm):
    spell = StringField(validators=[DataRequired('iv'), Length(1, 32, 'iv')])


class PaperPfIdForm(BaseForm):
    pf_id = StringField(validators=[DataRequired('iv'), Length(1, 36, 'iv')])


class PaperSpellForm(PaperPfIdForm):
    spell = StringField(validators=[DataRequired('iv'), Length(1, 32, 'iv')])


class BlogAlbumPostForm(PageForm):
    name = StringField(validators=[DataRequired(), Length(min=1, max=32)])

    def validate_album_name(self, field):
        if len(field.errors) != 0:
            return
        BlogAlbum.query.with_entities(BlogAlbum.id).filter_by(name=field.data).first_or_404()


class PaperAlbumForm(PageForm):
    name = StringField(validators=[DataRequired(), Length(min=1, max=32)])

    def validate_album_name(self, field):
        if len(field.errors) != 0:
            return
        PaperAlbum.query.with_entities(PaperAlbum.id).filter_by(name=field.data).first_or_404()


# class MessageForm(BaseForm):
#     texter_name = StringField(validators=[DataRequired(), Length(min=1, max=32)])
#     text = StringField(validators=[DataRequired(), Length(min=1, max=360)])
#
#     def validate_text(self, field):
#         if len(field.errors) != 0:
#             return
#         print()