from packaging.version import parse

import pytest

from ai.data import DataProcessor
from ai.common.github import GitHubRepository
from api.models.config import ApiAutoTestConfig

dp = DataProcessor()


class TestSecurity:
    
    @pytest.mark.parametrize('test_data', dp.read_test_data(path='chat/security/cve'))
    def test_langchain_cve(self, test_config: ApiAutoTestConfig, test_data: dict):

        def _find_package_version(lock_content: str, package_name: str) -> str:
            """Find the version of a specific package from the poetry.lock content"""
            lines = lock_content.splitlines()
            for i, line in enumerate(lines):
                if line.strip() != f'name = "{package_name}"':
                    continue
                version_line = lines[i + 1]
                if 'version =' in version_line:
                    return version_line.split('=')[1].strip().strip('"')
            raise ValueError(f'Package {package_name} not found in the poetry.lock content')
        
        def _parse_risk_rules(version: str, rules: dict) -> bool:
            """Parse risk rules from the test data"""
            version_parsed = parse(version)
            for operator, rule_version in rules.items():
                rule_parsed = parse(rule_version)
                match operator:
                    case 'gt' if version_parsed <= rule_parsed:
                        return False
                    case 'gte' if version_parsed < rule_parsed:
                        return False
                    case 'lt' if version_parsed >= rule_parsed:
                        return False
                    case 'lte' if version_parsed > rule_parsed:
                        return False
                    case 'eq' if version_parsed != rule_parsed:
                        return False
            return True

        poetry_lock_content = GitHubRepository(
            repo_name='XXXXXXXX', 
            repo_owner='XXXXXX'
        ).get_file_content(
            file_path='poetry.lock',
            branch=test_config.environment
        )
        langchain_version = _find_package_version(lock_content=poetry_lock_content, package_name='langchain')
        assert _parse_risk_rules(langchain_version, test_data['cve']['rule']) is False, f'fail: ({test_data['case_no']}), {test_data['case_desc']} version: {langchain_version}, rules: {test_data['cve']['rule']}'
