import pytest
from dotenv import load_dotenv

from common.manager import ConfigManager
from api.models.config import ServiceConfig, ApiAutoTestConfig


@pytest.fixture(scope='session', autouse=True)
def test_config(pytestconfig: pytest.Config) -> ApiAutoTestConfig:
    load_dotenv()

    test_env = pytestconfig.getoption('--environment')
    test_services = pytestconfig.getoption('--services')

    cfg_data = ConfigManager().read(test_type='api', file_name='api_services')
    
    return ApiAutoTestConfig(
        environment=test_env,
        services=ServiceConfig(
            name=test_services,
            auth_url=cfg_data[test_services]['auth_url'][test_env],
            base_url=cfg_data[test_services]['base_url'][test_env],
            timeout=cfg_data[test_services]['timeout']
        )
    )

@pytest.fixture(scope='session', autouse=True)
def search_test_config(pytestconfig: pytest.Config) -> ApiAutoTestConfig:
    load_dotenv()

    test_env = pytestconfig.getoption('--environment')

    cfg_data = ConfigManager().read(test_type='api', file_name='api_services')
    
    return ApiAutoTestConfig(
        environment=test_env,
        services=ServiceConfig(
            name='search',
            auth_url=cfg_data['search']['auth_url'][test_env],
            base_url=cfg_data['search']['base_url'][test_env],
            timeout=cfg_data['search']['timeout']
        )
    )