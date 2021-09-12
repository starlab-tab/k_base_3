import json

import requests
from app.exceptions import Code404
from app.utils.crawler import BaseAnalyst, DANDict


class JsonAnalyst(BaseAnalyst):

    def fetch_with_get(self, params=None, func=None):
        resp = requests.get(
            url=self.get_api(),
            params=params,
            headers=self.headers
        )
        resp.encoding = 'utf-8'
        if resp.status_code == 200:
            if func:
                func(resp.json())
            self.raw_data = resp.json()
            self.start()
        else:
            raise Code404('request api fail')
        # with open('E:/JetBrains_PP/PyCharm/fb.json', encoding='utf-8') as json_file:
        #     self.raw_data = json.load(json_file)
        # self.start()

    def fetch_with_post(self, params=None):
        resp = requests.post(
            self.get_api(),
            params=params,
            data=self.data,
            headers=self.headers
        )
        resp.encoding = 'utf-8'
        if resp.json()['code'] == 200:
            self.raw_data = resp.json()

    def get_base_attr(self):
        json_data = DANDict(self.raw_data)
        for key, value in self.crawler.rules.items():
            self.data_to_load[key] = json_data.get(value)