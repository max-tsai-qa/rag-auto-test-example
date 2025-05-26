import os
import pytest
import time
import re
from pathlib import Path
import json
import allure


CASE_DETAIL_REQUIRED_FIELDS = ['id', 'desc', 'tags', 'priority']
EXPECT_RESULT_REQUIRED_FIELDS = ['status_code', 'response_schema']

def pytest_addoption(parser: pytest.Parser):
    parser.addoption('--environment', choices=('prod', 'uat', 'stg', 'dev'), help='Choices test environment', required=True)
    parser.addoption('--services', help='Choices test services', required=True)
    parser.addoption('--tags', help='Specific testdata with tags need to test, if need to input multiple tags, plz using "," ', required=False)
    parser.addoption('--trace-api', default=False, action='store_true', help='If true than trace api log.')

def pytest_collection_modifyitems(config, items):
    selected_service = config.getoption('--services')
    tags = config.getoption('--tags')
    filtered_items = []

    if tags:
        tags = tags.split(',')

    def _validate_fields(data: dict, required_fields: list):
        # Check testdata contain require_fields or not
        for field in required_fields:
            if field not in data:
                raise KeyError(f'Error: Missing field "{field}" in case: {data}')

    for item in items:
        if selected_service != item.nodeid.split('/')[1]:
            continue

        test_name_group = re.search(r'test_(.+?)\.py::\w+::test_(.+?)\[(.+?)\]', item.nodeid)
        if not test_name_group:
            continue  # Skip if the regex pattern doesn't match

        feature, test_api, _ = test_name_group.groups()
        json_path = Path(__file__).parent / f'data/{selected_service}/{feature}/{test_api}.json'

        if json_path.exists():
            with json_path.open('r') as f:
                test_data = json.load(f)
            metadata = test_data.get('metadata', {})
            case_data = next((case for case in test_data['dataset']
                              if item.name == f'test_{test_api}[test_data{case['case_detail']['id']}]'), None)

            if not case_data:
                continue

            case_detail = case_data['case_detail']

            _validate_fields(data=case_detail, required_fields=CASE_DETAIL_REQUIRED_FIELDS)
            _validate_fields(data=case_data['expect_result'], required_fields=EXPECT_RESULT_REQUIRED_FIELDS)

            if tags and not (set(tags) & set(case_detail['tags'])):
                continue

            item.add_marker(allure.tag(*case_detail.get('tags', [])))
            item.add_marker(allure.parent_suite(f'{feature.upper()} API'))
            item.add_marker(allure.suite(test_api))
            item.add_marker(allure.label('owner', metadata.get('owner', '')))
            item.add_marker(allure.description(f'{metadata['method']} {metadata['path']}'))
            item.add_marker(allure.severity(case_detail.get('priority', 'medium')))

            filtered_items.append(item)

    if not filtered_items:
        pytest.skip(f'No tests found for the service "{selected_service}"')

    items[:] = filtered_items

def pytest_terminal_summary(terminalreporter, config):
    # Check for pytest-xdist plugin, to avoid sending a report for each worker.
    if hasattr(terminalreporter.config, 'workerinput'):
        return

    def _count_tests(outcome, condition=lambda i: i.when == 'call'):
        return len([i for i in terminalreporter.stats.get(outcome, []) if condition(i)])
    
    passed = _count_tests('passed')
    failed = _count_tests('failed')
    skipped = _count_tests('skipped')

    # send test result message
