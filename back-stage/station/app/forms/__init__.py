import re

from flask import request
from wtforms import Form, IntegerField, StringField, FieldList, BooleanField
from wtforms.validators import DataRequired, NumberRange, Length, ValidationError, AnyOf, Regexp, URL, InputRequired

from app.exceptions import Code400, Code404
from app.models import Crawler, db, Paper


class BaseForm(Form):
    def __init__(self, data=None):
        if not data:
            data = request.get_json(silent=True)
        super(BaseForm, self).__init__(data=data)

    def validate_for_api(self):
        valid = super(BaseForm, self).validate()
        if not valid:
            raise Code400(msg=self.errors)
        return self.data


class AuthForm(BaseForm):
    ident = StringField(validators=[DataRequired('param invalid'),
                                    Length(1, 2048, 'param invalid')])

    auth = StringField(validators=[DataRequired('param invalid'),
                                   Length(1, 2048, 'param invalid')])


class IdForm(BaseForm):
    id = IntegerField(validators=[DataRequired('missing id'), NumberRange(1, 10000, 'id invalid')])


class PageForm(BaseForm):
    page = IntegerField(validators=[NumberRange(0, 1000, 'page num invalid')])


class SearchForm(PageForm):
    tracker = StringField(validators=[DataRequired('tracker invalid'), Length(1, 32, 'tracker invalid')])


class UpdateAlbumForm(IdForm):
    album_name = StringField(validators=[DataRequired('missing album name'), Length(1, 50, 'album name invalid')])


class UploadImageForm:
    white_list = ['.png', '.jpeg', '.jpg', '.gif', '.webp', 'jfif']
    white_type = ['image/png', 'image/jpeg', 'image/gif', 'image/webp', 'image/jfif']
    params = 'image'

    def __init__(self, params=None, white_list=None, white_type=None):
        if white_list:
            self.white_list = white_list
        if white_type:
            self.white_type = white_type
        if params:
            self.params = params

    def validate_for_api(self, file):
        if len(file) != 1 or self.params not in file:
            raise Code400()
        image = file[self.params]
        suffix = image.filename[image.filename.rfind('.'):].lower()
        mime_type = image.mimetype.lower()
        content_type = image.content_type.lower()
        valid_suffix = True if suffix in self.white_list else False
        valid_type = True if mime_type in self.white_type and content_type == mime_type else False
        if valid_suffix and valid_type:
            return True
        else:
            raise Code404()


class AlsImageForm(BaseForm):
    url = StringField(
        validators=[Regexp('https?:\\/\\/\\S*?\\/[a-z0-9\\/_\\?=-]*(?:\\.png|\\.jpg|\\.jpeg|\\.webp|\\.gif|\\.jfif)',
                           re.IGNORECASE, 'invalid image'), Length(max=200)])


class ActiveCrawlerForm(BaseForm):
    platform = StringField(validators=[DataRequired('invalid'), Length(1, 20, 'invalid')])
    part_url = StringField(validators=[DataRequired('invalid'), Length(1, 50, 'invalid')])
    id = StringField(validators=[DataRequired('invalid'), Length(1, 32, 'invalid')])

    def validate_id(self, field):
        if len(field.errors) != 0:
            return
        # 可先验证id长度是否符合该平台的crawler规则
        if Paper.query.with_entities(Paper.id).filter_by(pf_id=field.data).first():
            raise ValidationError('record exist')
