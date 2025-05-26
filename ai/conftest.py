import pytest

def pytest_addoption(parser: pytest.Parser):
    parser.addoption('--environment', choices=('prod', 'uat', 'stg', 'dev'), help='Choices test environment', required=True)
    parser.addoption('--services', help='Choices test services', required=True)


def pytest_collection_modifyitems(config, items):
    selected_service = config.getoption('--services')
    
    if selected_service:
        selected_items = []
        deselected_items = []
        for item in items:
            if not selected_service or selected_service in item.nodeid:
                selected_items.append(item)
            else:
                deselected_items.append(item)
        if deselected_items:
            config.hook.pytest_deselected(items=deselected_items)
            items[:] = selected_items
    

def pytest_terminal_summary(terminalreporter, config):
    # Check for pytest-xdist plugin, to avoid sending a report for each worker.
    if hasattr(terminalreporter.config, 'workerinput'):
        return

    def _count_tests(outcome, condition=lambda i: i.when == 'call'):
        return len([i for i in terminalreporter.stats.get(outcome, []) if condition(i)])
    
    passed = _count_tests('passed')
    failed = _count_tests('failed')
    skipped = _count_tests('skipped')
    
    # send test result meesage