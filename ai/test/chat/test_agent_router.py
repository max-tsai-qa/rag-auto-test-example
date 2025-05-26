import pytest

from ai.data import DataProcessor
from api.apis.chat.chat import Chat
from api.models.config import ApiAutoTestConfig

dp = DataProcessor()


@pytest.fixture(scope='class', autouse=True)
def chat(test_config: ApiAutoTestConfig) -> Chat:
    chat = Chat(config=test_config)
    chat.cached_token = chat.get_token()
    return chat


class TestAgentRouter:
    
    @pytest.mark.parametrize('test_data', dp.read_test_data(path='chat/agent_router/link_1'))
    def test_link_1(self, chat: Chat, test_data: dict):
        """ link_1:
        agent_1 -> agent_2 -> agent_3
        """
        conversation_id = chat.conversations.post_conversations(auth=chat.cached_token, user_id='auto_test_user_id').json()['conversation_id']
        messages = [
            {
                'content': {
                    'type': 'plain-text',
                    'text': test_data['param_text_input']
                },
                'author': 'human'
            }
        ]
        res = chat.conversations.post_messages(
            auth=chat.cached_token,
            conversation_id=conversation_id,
            messages=messages,
            streaming=False
        )
        call_link = res['call_link']

        assert call_link == test_data['expect_call_link'], f'Expect call link: {test_data['expect_call_link']}, but got {call_link}'
