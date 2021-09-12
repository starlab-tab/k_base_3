from app.utils.crawler.html_analyst import HtmlAnalyst


def correct_image(img):
    return img.attrs.get('data-src', None)


class Analyst(HtmlAnalyst):
    # datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data_to_load = {'date': 'no date'}

    def als_image(self, media_type=None, func=None):
        super().als_image(media_type=media_type, func=correct_image)

    def rebuild_pre_tag(self):
        for pre in self.content_soup.find_all('pre'):
            if pre.parent.name == 'section'\
                    and len(pre.parent.contents) > 0\
                    and pre.parent.contents[0].name == 'ul':
                del pre.parent.contents[0]
            pre.attrs = {'class': 'language-'}
            text = '\n'.join(code.text for code in pre.find_all('code'))
            new_code = self.content_soup.new_tag(name='code')
            new_code.string = text
            pre.contents = [new_code]