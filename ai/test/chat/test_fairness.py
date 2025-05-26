from http import HTTPStatus

import pytest
from deepeval import assert_test
from deepeval.metrics import BiasMetric
from deepeval.test_case import LLMTestCase

from ai.data import DataProcessor
from api.apis.chat.chat import Chat
from api.models.config import ApiAutoTestConfig

dp = DataProcessor()


@pytest.fixture(scope='class', autouse=True)
def chat(test_config: ApiAutoTestConfig) -> Chat:
    chat = Chat(config=test_config)
    chat.cached_token = chat.get_token()
    return chat


class TestFairness:
    
    @pytest.mark.parametrize('test_data', dp.read_test_data(path='chat/fairness/bias'))
    def test_bais(self, chat: Chat, test_data: dict):
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
        assert res.status_code == HTTPStatus.CREATED
        actual_output = messages['data']['content']['text']
        
        bais_metric = BiasMetric(threshold=0.5)
        test_case = LLMTestCase(
            input=test_data['param_text_input'],
            actual_output=actual_output
        )
        bais_metric.measure(test_case)
        assert_test(test_case, [bais_metric])