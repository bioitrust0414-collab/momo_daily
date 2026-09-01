from pathlib import Path
import yaml

ROOT = Path('/home/ubuntu/momo_daily_latest')
CAL = ROOT / 'schedule/content-calendar.yaml'
ARC = ROOT / 'schedule/archive.yaml'
POST_ID = 'momo-20260901'
PERMALINK = 'https://www.instagram.com/p/DcuYmm1FIdt/'

with CAL.open(encoding='utf-8') as f: cal = yaml.safe_load(f) or {'posts': []}
with ARC.open(encoding='utf-8') as f: arc = yaml.safe_load(f) or {'posts': []}
posts = cal.get('posts', []) if isinstance(cal, dict) else cal
archives = arc.get('posts', []) if isinstance(arc, dict) else arc
post = next((p for p in posts if p.get('id') == POST_ID), None)
if post is None: raise SystemExit(f'找不到 {POST_ID}')
if any(p.get('id') == POST_ID for p in archives): raise SystemExit(f'{POST_ID} 已存在於 archive，停止避免重複')
post = dict(post)
post['status'] = 'published'
post['permalink'] = PERMALINK
archives.append(post)
cal['posts'] = [p for p in posts if p.get('id') != POST_ID]
arc['posts'] = archives
with CAL.open('w', encoding='utf-8') as f: yaml.safe_dump(cal, f, allow_unicode=True, sort_keys=False)
with ARC.open('w', encoding='utf-8') as f: yaml.safe_dump(arc, f, allow_unicode=True, sort_keys=False)
print('archived', POST_ID, PERMALINK)
