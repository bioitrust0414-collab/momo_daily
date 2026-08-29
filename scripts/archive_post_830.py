import datetime
from pathlib import Path
import yaml

ROOT = Path('/home/ubuntu/momo_daily_latest')
CALENDAR_PATH = ROOT / 'schedule/content-calendar.yaml'
ARCHIVE_PATH = ROOT / 'schedule/archive.yaml'
POST_ID = 'momo-20260830'
PERMALINK = 'https://www.instagram.com/p/DcpFPaTlGEO/'

with CALENDAR_PATH.open(encoding='utf-8') as f:
    calendar = yaml.safe_load(f) or {'posts': []}
with ARCHIVE_PATH.open(encoding='utf-8') as f:
    archive = yaml.safe_load(f) or {'posts': []}

posts = calendar.get('posts', []) if isinstance(calendar, dict) else calendar
post = next((p for p in posts if p.get('id') == POST_ID), None)
if post is None:
    raise SystemExit(f'找不到 {POST_ID}，未修改檔案')

post['status'] = 'published'
post['published_at'] = datetime.datetime.now(datetime.timezone.utc).astimezone().isoformat()
post['permalink'] = PERMALINK
archive.setdefault('posts', []).append(post)
if isinstance(calendar, dict):
    calendar['posts'] = [p for p in posts if p.get('id') != POST_ID]
else:
    calendar = [p for p in posts if p.get('id') != POST_ID]

with CALENDAR_PATH.open('w', encoding='utf-8') as f:
    yaml.safe_dump(calendar, f, allow_unicode=True, sort_keys=False)
with ARCHIVE_PATH.open('w', encoding='utf-8') as f:
    yaml.safe_dump(archive, f, allow_unicode=True, sort_keys=False)
print(f'已歸檔 {POST_ID}: {PERMALINK}')
