import requests
from app.exceptions import Code404
from app.utils.crawler import BaseAnalyst
from bs4 import BeautifulSoup as bs4


class HtmlAnalyst(BaseAnalyst):

    def fetch_with_get(self, params=None):
        resp = requests.get(
            url=self.get_api(),
            params=params,
            headers=self.headers,
        )
        resp.encoding = 'utf-8'
        if resp.status_code == 200:
            self.raw_data = bs4(resp.text, "lxml")
            self.start()
        else:
            raise Code404(f'invalid {self.crawler.platform} paper url')
        # with open('E:/JetBrains_PP/PyCharm/PycharmProjects/KnowBase/xz_data.txt', encoding='utf-8') as infile:
        #     self.raw_data = bs4(infile.read(), "lxml")
        #     self.start()

    def fetch_with_post(self):
        pass

    def get_base_attr(self):
        for key, value in self.crawler.rules.items():
            selector = self.raw_data.select_one(value)
            if not selector:
                text = f'{key} selector changed'
            else:
                if key == 'content':
                    text = '\n'.join(str(tag).strip() for tag in selector.children)
                    if len(text) == 0:
                        text = f'{key} empty'
                else:
                    text = selector.text.strip() if len(selector.text.strip()) != 0 else f'{key} empty'
            self.data_to_load[key] = text

    def get_api(self):
        p = f'{self.crawler.api}{self.data_to_load["pf_id"]}'
        return f'{self.crawler.api}{self.data_to_load["pf_id"]}'
