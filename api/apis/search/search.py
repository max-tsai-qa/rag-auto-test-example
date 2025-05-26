from urllib.parse import urljoin

from ..base import BaseApi
from api.models.config import ApiAutoTestConfig


class SearchApi(BaseApi):

    VERSION = 'v1'
    SEARCH_API = f'{VERSION}/search'

    def post_text(self, body: dict):
        """
        :param body:
        """
        url = urljoin(self._base_url, f'{self.SEARCH_API}/text')
        res = self._request(method='POST', url=url, json=body)
        return res

class Search(BaseApi):
    """
    api swagger: https://
    """

    def __init__(self, config: ApiAutoTestConfig) -> None:
        super().__init__(config)
        self._search = SearchApi(config)

    @property
    def search(self) -> SearchApi:
        return self._search
    
    def get_health_check(self):
        url = urljoin(self._base_url, '/health_check')
        res = self._request(method='GET', url=url)
        return res
