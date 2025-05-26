import os
import json
import logging
from shlex import quote

import allure
import pytest
import requests

from api.models.config import ApiAutoTestConfig


class BaseApi:

    def __init__(self, config: ApiAutoTestConfig) -> None:
        self._config = config
        self._auth_url = config.services.auth_url
        self._base_url = config.services.base_url
        self._timeout = config.services.timeout
        self._session = requests.Session()

    @staticmethod
    def _convert_request_to_curl(response: requests.Response) -> str:
        request = response.request
        parts = [
            'curl',
            '-X', quote(request.method)
        ]

        # headers
        parts.extend(f'-H {quote(f'{k}: {v}')}' for k, v in sorted(request.headers.items()))

        # body
        if request.body:
            body = request.body.decode('utf-8') if isinstance(request.body, bytes) else request.body
            parts.extend(['-d', quote(body)])

        parts.append(quote(request.url))
        return ' '.join(parts)

    def _log_response_details(self, request: dict, response: requests.Response):
        try:
            response_body = json.dumps(response.json(), indent=4, ensure_ascii=False)
        except json.JSONDecodeError:
            response_body = f'{response.text[:300]}...'

        if request_headers := request.get('headers'):
            request_headers = json.dumps(request_headers, indent=4)

        if json_payload := request.get('json'):
            json_payload = json.dumps(obj=json_payload, indent=4, ensure_ascii=False)

        details = {
            'request-headers': request_headers or 'N/A',
            'request-json': json_payload or 'N/A',
            'request-data': request.get('data') or 'N/A',
            'request-to-curl': self._convert_request_to_curl(response),
            'response-status': f'{response.status_code} {response.reason}',
            'response-time': f'{response.elapsed.total_seconds()}s',
            'response-body': response_body
        }

        with allure.step(f'[{request["method"].upper()}] {request["url"]}'):
            allure.attach(
                json.dumps(details),
                name='Request & Response Details',
                attachment_type=allure.attachment_type.JSON
            )

        logging.info(f'\n\n\n[{request["method"].upper()}] {request["url"]}')
        logging.info('\n'.join(f'{k}: {v}' for k, v in details.items()))

    def _request(self, method: str, url: str, timeout: int | None = None, **kwargs) -> requests.Response:
        request_timeout = timeout or self._timeout
        try:

            resp = self._session.request(method, url, timeout=request_timeout, **kwargs)
            if self._config.trace is True:
                self._log_response_details(
                    request={'method': method, 'url': url, **kwargs},
                    response=resp
                )
        except requests.RequestException as e:
            pytest.fail(f'request error, {str(e)}')
        return resp

    def _get_env_var(self, var_name: str):
        env_prefix = f'{self._config.services.name.upper()}_{self._config.environment.upper()}'
        return os.getenv(f'{env_prefix}_{var_name}')
