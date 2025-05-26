import json
from pathlib import Path


class DataProcessor:

    def read_test_data(self, path: str) -> list[dict]:
        full_path = Path(__file__).parent / f'{path}.json'
        if not full_path.exists():
            raise FileNotFoundError(f'Test data not found: {full_path}')

        with open(file=full_path, mode='r', encoding='utf-8') as json_file:
            raw_data = json.load(fp=json_file)

        # Remove skipped cases (case_state == 0)
        filtered_data = [case for case in raw_data['dataset'] if case['case_state'] != 0]
        
        return filtered_data
