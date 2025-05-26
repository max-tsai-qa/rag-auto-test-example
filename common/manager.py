from pathlib import Path
from typing import Any, Dict

import yaml


class SingletonMeta(type):

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class ConfigManager(metaclass=SingletonMeta):

    def __init__(self) -> None:
        self._cache = {}
        
    def _load(self, path: Path) -> Any:
        try:
            with open(file=path, mode='r') as stream:
                return yaml.safe_load(stream=stream)
        except yaml.YAMLError as e:
            raise RuntimeError(f'Error parsing YAML file: {path}') from e
        except Exception as e:
            raise RuntimeError(f'Error reading file: {path}') from e

    def read(self, test_type: str, file_name: str) -> Dict[str, Any]:
        if test_type not in ['ai', 'api', 'app', 'web']:
            raise ValueError(f'Invalid test type values: {test_type}. only [ai, api, app, web] are allowed')
        if file_name not in self._cache:
            file_path = Path(__file__).parent.parent / test_type / f'configurations/{file_name}.yaml'
            if not file_path.exists():
                raise FileNotFoundError(f'Configuration file not found: {file_path}')
            self._cache[file_name] = self._load(path=file_path)
        return self._cache[file_name]
