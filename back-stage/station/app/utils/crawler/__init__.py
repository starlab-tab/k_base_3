from app import db
from app.exceptions import Code404
from app.models import Paper, PaperAlbum
from app.schemas.sec.archive import PaperSchema, load_paper_with_check, dump_paper_with_check
from app.utils import safe_image
from bs4 import BeautifulSoup as bs4


class BaseAnalyst:
    pape = None
    crawler = None
    raw_data = None
    data_to_load = dict()
    dump_data = None
    content_soup = None
    media_type = 'sec'
    params = None,
    data = None
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 7.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'
    }

    def __init__(self, pf_id=None, part_url=None, crawler=None):
        if not (pf_id and part_url and crawler):
            raise Code404('missing parama')
        self.crawler = crawler
        self.data_to_load['pf_id'] = pf_id
        self.data_to_load['pf_name'] = crawler.platform
        self.data_to_load['pf_url'] = f'{crawler.base_url}{part_url}{pf_id}'

    def start(self):
        self.get_base_attr()
        self.als_content()
        self.seal()

    def get_base_attr(self):
        pass

    def als_content(self):
        self.correct_raw_data()
        self.content_soup = bs4(self.data_to_load['content'], "lxml")
        self.clean_content()
        self.als_image()
        self.rebuild_pre_tag()
        self.rebuild_content()

    def correct_raw_data(self):
        self.data_to_load['title'] = self.data_to_load['title'][:128].strip()
        self.data_to_load['date'] = self.data_to_load['date'][:32].strip()
        self.data_to_load['content'] = self.data_to_load['content'][:199800].strip()
        self.data_to_load['visible'] = True
        load_paper_with_check(PaperSchema(exclude=['id']), self.data_to_load)

    def clean_content(self):
        for tag in self.crawler.pure_tags:
            for raw_tag in self.content_soup.find_all(tag):
                raw_tag.attrs = {}

    def rebuild_pre_tag(self):
        for pre in self.content_soup.find_all('pre'):
            pre.attrs = {'class': 'language-'}
            new_code = self.content_soup.new_tag(name='code')
            text = ''
            if pre.next.name == 'span':
                text = pre.text
            elif pre.next.name == 'code':
                text = '\n'.join(code.text for code in pre.find_all('code'))
            if len(text) == 0: text = pre.text
            new_code.string = text
            pre.contents = [new_code]

    def als_image(self, media_type=None, func=None):
        if media_type:
            self.media_type = media_type
        for img in self.content_soup.find_all('img'):
            image_src = img.attrs.get('src', None)
            if func:
                image_src = func(img)
            img.attrs = {}
            if not image_src: continue
            if image_src.startswith('data:image'):
                image_url, status = safe_image.for_base64(media_type=self.media_type, base64_str=image_src)
            else:
                image_src = image_src if not image_src.startswith('/') else f'{self.crawler.base_url}{image_src}'
                image_url, status = safe_image.for_url(self.media_type, image_url=image_src)
            if status:
                img['src'] = image_url
            else:
                img['alt'] = image_url

    def rebuild_content(self):
        try:
            self.data_to_load['content'] = '\n'.join(str(tag).strip() for tag in self.content_soup.html.body)
        except Exception as e:
            self.data_to_load['content'] = '<h2>Fail To Rebuild Content</h2>'

    def seal(self):
        paper = load_paper_with_check(PaperSchema(exclude=['id']), self.data_to_load)
        paper_album = PaperAlbum(name=self.crawler.platform)
        query_album = PaperAlbum.query.filter_by(name=self.crawler.platform).first()
        if query_album:
            paper.albums.append(query_album)
        else:
            paper.albums.append(paper_album)
        with db.auto_commit():
            db.session.add(paper)
        paper = Paper.query.filter_by(pf_id=paper.pf_id).first_or_404()
        self.dump_data = dump_paper_with_check(PaperSchema(exclude=['pf_id', 'pf_name']), paper)
        self.dump_data['albums'] = list(map(lambda x: x['name'], self.dump_data['albums']))

    def get_api(self):
        return self.crawler.api


# https://stackoverflow.com/questions/39818669/dynamically-accessing-nested-dictionary-keys
# DynamicAccessNestedDict
class DANDict:

    def __init__(self, data):
        self.data = data

    def get(self, keys):
        try:
            data = self.data
            for k in keys:
                data = data[k]
        except KeyError as e:
            data = f'{keys[-1]} chain changed'
        return data

    # def set(self, keys, val):
    #     data = self.data
    #     lastkey = keys[-1]
    #     for k in keys[:-1]:  # when assigning drill down to *second* last key
    #         data = data[k]
    #     data[lastkey] = val
