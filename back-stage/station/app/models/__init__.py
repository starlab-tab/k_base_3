from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy, BaseQuery
from contextlib import contextmanager
from sqlalchemy import text
from sqlalchemy.sql import expression
from werkzeug.security import generate_password_hash, check_password_hash
from app.exceptions import Code404
from app.token import jwt


class SQLAlchemy(_SQLAlchemy):
    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            print("rollback")
            db.session.rollback()
            raise e


class Query(BaseQuery):
    def get_or_404(self, ident, description=None):
        rv = self.get(ident)
        if not rv:
            raise Code404(msg=description)
        return rv

    def first_or_404(self, description=None):
        rv = self.first()
        if not rv:
            raise Code404(msg=description)
        return rv


db = SQLAlchemy(query_class=Query)
ma = Marshmallow()


class TokenBlocklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, server_default=db.func.now())


@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    token = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()
    return token is not None


class MalIp(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(16), nullable=False, server_default=text('"1.1.1.1"'))
    num = db.Column(db.Integer, nullable=True, server_default=text('1'))
    xffs = db.Column(db.JSON, nullable=True)
    agents = db.Column(db.JSON, nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime(timezone=True), nullable=True, onupdate=db.func.now())


class Neddle(db.Model):
    __tablename__ = "neddle"
    id = db.Column(db.Integer, primary_key=True)
    ident = db.Column(db.String(16), nullable=False)
    _auth = db.Column('auth', db.String(128), nullable=False)

    def __init__(self, **kwargs):
        super(Neddle, self).__init__(**kwargs)

    @property
    def auth(self):
        return self._auth

    @auth.setter
    def auth(self, raw):
        self._auth = generate_password_hash(raw)

    def valid_auth(self, raw):
        return check_password_hash(self._auth, raw)


Blog_M_Album = db.Table('blog_m_album',
                        db.Column('blog_album_id', db.Integer, db.ForeignKey('blog_album.id'), primary_key=True),
                        db.Column('blog_id', db.Integer, db.ForeignKey('blog.id'), primary_key=True),
                        db.Column('created_at', db.DateTime(timezone=True), nullable=False,
                                  server_default=db.func.now())
                        )


class BlogAlbum(db.Model):
    __tablename__ = "blog_album"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False,server_default=db.func.now())
    updated_at = db.Column(db.DateTime(timezone=True), nullable=True,onupdate=db.func.now())

    def __init__(self, **kwargs):
        super(BlogAlbum, self).__init__(**kwargs)

    def __repr__(self):
        return f'<BlogAlbum {self.name}>'


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(130), nullable=False)
    cover = db.Column(db.String(128), nullable=True)
    maker = db.Column(db.String(24), nullable=True)
    visible = db.Column(db.Boolean, nullable=False, server_default=expression.true())
    protection = db.Column(db.String(14), nullable=True, server_default=text('""'))
    desc = db.Column(db.String(180), nullable=True, server_default=text('""'))
    content = db.Column(db.Text(200000), nullable=False)
    albums = db.relationship('BlogAlbum', secondary=Blog_M_Album, lazy='select',backref=db.backref('blogs', lazy=True))
    images = db.Column(db.JSON, nullable=True)
    chips = db.Column(db.JSON, nullable=True)
    views = db.Column(db.Integer, nullable=True, server_default=text('1'))
    created_at = db.Column(db.DateTime(timezone=True), nullable=False,server_default=db.func.now())
    updated_at = db.Column(db.DateTime(timezone=True), nullable=True,onupdate=db.func.now())

    def __init__(self, **kwargs):
        super(Blog, self).__init__(**kwargs)

    def __repr__(self):
        return '<Blog %r>' % self.title


class Crawler(db.Model):
    __tablename__ = "crawler"
    id = db.Column(db.Integer, primary_key=True)
    platform = db.Column(db.String(36), nullable=False)
    base_url = db.Column(db.String(66), nullable=False)
    url_reg = db.Column(db.String(130), nullable=False)
    type = db.Column(db.String(8), nullable=False, server_default=text('"json"'))
    api = db.Column(db.String(130), nullable=False)
    pure_tags = db.Column(db.JSON, nullable=False)
    rules = db.Column(db.JSON, nullable=True)
    custom = db.Column(db.Boolean, nullable=False, server_default=expression.false())
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime(timezone=True), nullable=True, onupdate=db.func.now())


Paper_M_Album = db.Table('paper_m_album',
                         db.Column('paper_album_id', db.Integer, db.ForeignKey('paper_album.id'), primary_key=True),
                         db.Column('paper_id', db.Integer, db.ForeignKey('paper.id'), primary_key=True),
                         db.Column('created_at', db.DateTime(timezone=True), nullable=False,
                                   server_default=db.func.now())
                         )


class PaperAlbum(db.Model):
    __tablename__ = "paper_album"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    papers = db.relationship('Paper', secondary=Paper_M_Album, lazy='select',backref=db.backref('albums', lazy=True))
    created_at = db.Column(db.DateTime(timezone=True), nullable=False,server_default=db.func.now())

    def __init__(self, **kwargs):
        super(PaperAlbum, self).__init__(**kwargs)

    def __repr__(self):
        return f'<PaperAlbum {self.name}>'


class Paper(db.Model):
    # pf -- paper_from
    id = db.Column(db.Integer, primary_key=True)
    pf_id = db.Column(db.String(40), nullable=False)
    pf_name = db.Column(db.String(20), nullable=False)
    pf_url = db.Column(db.String(130), nullable=False)
    author = db.Column(db.String(36), nullable=True)
    date = db.Column(db.String(36), nullable=True, server_default=text('"no date"'))
    title = db.Column(db.String(130), nullable=False)
    content = db.Column(db.Text(200000), nullable=False)
    chips = db.Column(db.JSON, nullable=True)
    visible = db.Column(db.Boolean, nullable=False, server_default=expression.true())
    protection = db.Column(db.String(14), nullable=True, server_default=text('""'))
    render = db.Column(db.Boolean, nullable=False, server_default=expression.false())
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime(timezone=True), nullable=True, onupdate=db.func.now())

    def __init__(self, **kwargs):
        super(Paper, self).__init__(**kwargs)

    def __repr__(self):
        return '<Paper %r>' % self.title


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(16), nullable=False, server_default=text('"1.1.1.1"'))
    texter = db.Column(db.String(40), nullable=False)
    text = db.Column(db.String(362), nullable=False)
    marked = db.Column(db.Boolean, nullable=False, server_default=expression.false())
    supervisor = db.Column(db.String(362), nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime(timezone=True), nullable=True, onupdate=db.func.now())

    def __init__(self, **kwargs):
        super(Message, self).__init__(**kwargs)

    def __repr__(self):
        return '<Message %r>' % self.text