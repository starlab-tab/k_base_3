from app.exceptions import Code400
from app.utils.crawler.json_analyst import JsonAnalyst


def check_api_response(resp):
    if not resp['success']:
        raise Code400('anquanke paper not exist')


class Analyst(JsonAnalyst):

    def __init__(self, pf_id=None, part_url=None, crawler=None):
        self.params = {'id': pf_id}
        super().__init__(pf_id=pf_id, part_url=part_url, crawler=crawler)

    def fetch_with_get(self, params=None, func=None):
        super().fetch_with_get(params=self.params, func=check_api_response)
