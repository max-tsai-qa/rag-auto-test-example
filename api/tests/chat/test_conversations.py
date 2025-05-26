import allure
from http import HTTPStatus
from pathlib import Path

import pytest

from api.apis.chat.chat import Chat
from api.data import DataProcessor
from api.models.config import ApiAutoTestConfig

dp = DataProcessor()


@pytest.fixture(scope='class', autouse=True)
def chat(test_config: ApiAutoTestConfig) -> Chat:
    chat = Chat(config=test_config)
    chat.cached_token = chat.get_token()
    return chat


class TestConversations:
    
    @pytest.mark.parametrize('test_data', dp.read_test_data(path='chat/conversations/post_conversations'))
    @allure.title('{test_data[case_desc]}')
    def test_post_conversations(self, chat: Chat, test_data: dict):
        token = chat.cached_token
        expect_result = test_data['expect_result']

        res = chat.conversations.post_conversations(auth=token)

        assert res.status_code == expect_result['status_code']
    
    @pytest.mark.parametrize('test_data', dp.read_test_data(path='chat/conversations/post_messages'))
    @allure.title('{test_data[case_desc]}')
    def test_post_messages(self, chat: Chat, test_data: dict):
        token = chat.cached_token
        pre_conditions = test_data['conditions']
        expect_result = test_data['expect_result']

        conversation_id = chat.conversations.post_conversations(
            auth=token, user_id='auto_test_user_id'
        ).json()['conversation_id']

        conversation_id = f'auto-{conversation_id}-not-found' \
            if pre_conditions['param_conversation_id'] != 'SCRIPT' else conversation_id

        for text in pre_conditions['param_content_text']:
            messages_content = [{
                'content': {
                    'type': pre_conditions['param_content_type'],
                    'text': text
                }
            }]
            res = chat.conversations.post_messages(auth=token, conversation_id=conversation_id, messages=messages_content)
            assert res.status_code == expect_result['status_code']
