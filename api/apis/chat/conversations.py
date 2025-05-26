from urllib.parse import urljoin

from ..base import BaseApi


class ConversationsApi(BaseApi):

    VERSION = 'v1'
    CONVERSATIONS_API = f'{VERSION}/conversations'

    def post_conversations(self, auth: str):
        """
        :param user_id:
            Which user created the conversations
        """
        return self._request(
            method='POST',
            url=urljoin(self._base_url, self.CONVERSATIONS_API),
            headers={'Authorization': auth},
        )
    
    def post_messages(
            self, auth: str,
            conversation_id: str,
            messages: list,
            streaming: bool = True,
            agents: dict = {}
    ):
        """
        :param user_id:
            Which user created the conversations
        :param conversation_id:
            The conversation space this message belongs to, create with post_conversations
        :param messages:
            The messages param with post message body param
        :param stream:
            The stream param with post message body param
        :param agents:
            The agents param with post message body param
        """
        body = {
            'agents': agents,
            'streaming': streaming,
            'messages': messages
        }
        return self._request(
            method='POST',
            url=urljoin(self._base_url, f'/{self.VERSION}/conversations/{conversation_id}/messages'),
            headers={'Authorization': auth},
            json=body,
        )
