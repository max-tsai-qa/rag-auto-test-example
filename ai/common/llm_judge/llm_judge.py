from abc import ABC, abstractmethod
import json
import os

from .prompt import POINTWISE_PROMPT


class LLMClient(ABC):

    def __init__(self) -> None:
        self.name = None

    @abstractmethod
    def generate_text(self, model: str, system_prompt: str, user_prompt: str):
        pass


class OpenAIAdapter(LLMClient):
    def __init__(self):
        from openai import OpenAI
        self.name = 'openai'
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    def generate_text(self, model: str, system_prompt: str, user_prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=model,
            messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': user_prompt}
            ],
            temperature=0.0,
            max_tokens=8192
        )
        return response.choices[0].message.content


class GeminiAdapter(LLMClient):
    def __init__(self):
        from google import genai
        self.name = 'gemini'
        self.client = genai.Client(
            vertexai=True, project='XXXXX', location='us-central1'
        )

    def generate_text(self, model: str, system_prompt: str, user_prompt: str) -> str:
        from google.genai import types
        response = self.client.models.generate_content(
            model=model, 
            contents=types.Content(
                role='user',
                parts=[types.Part.from_text(text=user_prompt)]
            ),
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                response_mime_type='application/json',
                max_output_tokens=8192,
                temperature=0.0,
            ),
        )
        return response.text


class LLMJudge:
    def __init__(self, client: LLMClient):
        self.client = client
    
    def pointwise(self, model: str, user_input: str, expected_output: str | None = None) -> dict:
        user_prompt = f"""
            帶入參數及值:
            user_input: {user_input}
            expected_output: {expected_output}
        """
        res = json.loads(
            self.client.generate_text(
                model=model,
                system_prompt=POINTWISE_PROMPT,
                user_prompt=user_prompt
            )
        )
        res['model_name'] = self.client.name
        return res
