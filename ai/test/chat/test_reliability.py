from http import HTTPStatus

import pytest
from deepeval import assert_test
from deepeval.metrics import FaithfulnessMetric
from deepeval.test_case import LLMTestCase

from ai.data import DataProcessor
from ai.common.llm_judge import LLMJudge, GeminiAdapter, OpenAIAdapter, assert_majority
from api.apis.chat.chat import Chat
from api.apis.search.search import Search
from api.models.config import ApiAutoTestConfig

dp = DataProcessor()


@pytest.fixture(scope='class', autouse=True)
def chat(test_config: ApiAutoTestConfig) -> Chat:
    chat = Chat(config=test_config)
    chat.cached_token = chat.get_token()
    return chat

@pytest.fixture(scope='class', autouse=True)
def search(search_test_config: ApiAutoTestConfig) -> Search:
    return Search(config=search_test_config)


class TestReliability:
    
    @pytest.mark.parametrize('test_data', dp.read_test_data(path='chat/reliability/faithfulness'))
    def test_faithfulness(self, chat: Chat, search: Search, test_data: dict):
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

        retrieval_context = search.search.post_text(body={
            'query': test_data['param_text_input'],
            'category': test_data['param_search_category']
        }).json()
        
        faithfulness_metric = FaithfulnessMetric(threshold=0.8)
        test_case = LLMTestCase(
            input=test_data['param_text_input'],
            actual_output=actual_output,
            retrieval_context=retrieval_context
        )
        faithfulness_metric.measure(test_case)
        assert_test(test_case, [faithfulness_metric])


    @pytest.mark.parametrize('test_data', dp.read_test_data(path='chat/reliability/pointwise'))
    def test_pointwises(self, chat: Chat, test_data: dict):
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

        gemini_judge = LLMJudge(GeminiAdapter())
        gemini_pointwise = gemini_judge.pointwise(
            model='gemini-2.0-flash',
            user_input=actual_output,
            expected_output=test_data['param_expected_output']
        )

        openai_judge = LLMJudge(OpenAIAdapter())
        openai_pointwise = openai_judge.pointwise(
            model='gpt-4o-mini',
            user_input=actual_output,
            expected_output=test_data['param_expected_output']
        )

        assert_majority(threshold=8, judges=[gemini_pointwise, openai_pointwise])
