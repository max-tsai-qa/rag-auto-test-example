from .conversations import ConversationsApi
from api.models.config import ApiAutoTestConfig
from ..base import BaseApi


class Chat(BaseApi):
    """
    api swagger: https://
    api wiki: https://
    """

    def __init__(self, config: ApiAutoTestConfig) -> None:
        super().__init__(config)
        self._conversations = ConversationsApi(config)

    @property
    def conversations(self) -> ConversationsApi:
        return self._conversations

    def get_token(self):
        # 這裡實踐 get token

        return 'Bearer XXXXXXXXX'
