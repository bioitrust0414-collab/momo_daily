from pathlib import Path
import yaml

path = Path('/home/ubuntu/momo_daily_latest/schedule/content-calendar.yaml')
with path.open(encoding='utf-8') as f:
    data = yaml.safe_load(f)
print('TYPE=', type(data).__name__)
if isinstance(data, dict):
    print('KEYS=', list(data.keys()))
    for key, value in data.items():
        print(f'KEY={key} TYPE={type(value).__name__} LEN={len(value) if hasattr(value, "__len__") else "NA"}')
elif isinstance(data, list):
    print('LEN=', len(data))
    print('IDS=', [item.get('id') for item in data if isinstance(item, dict)])
