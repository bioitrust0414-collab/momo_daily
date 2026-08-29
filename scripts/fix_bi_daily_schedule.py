from pathlib import Path
import yaml

ROOT = Path('/home/ubuntu/momo_daily_latest')
PATH = ROOT / 'schedule/content-calendar.yaml'
REMOVE = {'momo-20260831', 'momo-20260902', 'momo-20260904'}
KEEP = {'momo-20260901', 'momo-20260903', 'momo-20260905'}

with PATH.open(encoding='utf-8') as f:
    data = yaml.safe_load(f) or {'posts': []}
if not isinstance(data, dict) or not isinstance(data.get('posts'), list):
    raise SystemExit('content-calendar.yaml 格式錯誤')
posts = data['posts']
ids = {p.get('id') for p in posts}
missing = KEEP - ids
if missing:
    raise SystemExit(f'找不到應保留項目：{sorted(missing)}')
data['posts'] = [p for p in posts if p.get('id') not in REMOVE]
with PATH.open('w', encoding='utf-8') as f:
    yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False)
print('已移除：', ', '.join(sorted(REMOVE)))
print('保留：', ', '.join(sorted(KEEP)))
