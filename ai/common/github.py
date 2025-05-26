import os
import base64
from http import HTTPStatus

import requests


class GitHubRepository:

    def __init__(self, repo_name: str, repo_owner: str) -> None:
        self._base_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}'
        self._headers = {'Authorization': os.getenv(key='GITHUB_TOKEN')}

    def get_file_content(self, file_path: str, branch: str) -> str:
        res = requests.request(
            method='GET',
            url=f'{self._base_url}/contents/{file_path}',
            params={'ref': branch},
            headers=self._headers,
            timeout=10
        )
        if res.status_code == HTTPStatus.OK:
            return base64.b64decode(res.json()['content']).decode('utf-8')
        raise Exception(f'Failed to get file content: {res.text}')
