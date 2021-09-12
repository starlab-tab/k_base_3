from app.exceptions import Code400
from app.utils.crawler.json_analyst import JsonAnalyst


def clean_image(img):
    image_url = img.attrs.get('src', None)
    if not image_url and '!small' in image_url:
        return image_url.replace('!small', '')
    return image_url


def check_api_response(resp):
    if resp['code'] == 400:
        raise Code400('freebuf paper not exist')


class Analyst(JsonAnalyst):

    def __init__(self, pf_id=None, part_url=None, crawler=None):
        self.params = {'id': pf_id}
        super().__init__(pf_id=pf_id, part_url=part_url, crawler=crawler)

    def fetch_with_get(self, params=None, func=None):
        super().fetch_with_get(params=self.params, func=check_api_response)

    def als_image(self, media_type=None, func=None):
        super().als_image(media_type=media_type, func=clean_image)

    # def rebuild_pre_tag(self):
    #     for pre in self.content_soup.find_all('pre'):
    #         pre.attrs = {'class': 'language-'}
    #         text = '\n'.join(code.text for code in pre.find_all('code'))
    #         if len(text) == 0: text = pre.text
    #         new_code = self.content_soup.new_tag(name='code')
    #         new_code.string = text
    #         pre.contents = [new_code]
