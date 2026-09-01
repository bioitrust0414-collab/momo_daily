from pathlib import Path
from datetime import datetime, timezone

root = Path('/home/ubuntu/momo_daily_latest')
cal_path = root / 'schedule/content-calendar.yaml'
arc_path = root / 'schedule/archive.yaml'
post_id = 'momo-20260901'
permalink = 'https://www.instagram.com/p/DcuYmm1FIdt/'

cal = cal_path.read_text(encoding='utf-8')
start = cal.find(f'- id: {post_id}\n')
if start < 0:
    raise SystemExit(f'找不到 {post_id}')
next_start = cal.find('\n- id: ', start + 1)
if next_start < 0:
    next_start = len(cal)
cal_path.write_text(cal[:start] + cal[next_start + 1:], encoding='utf-8')

arc = arc_path.read_text(encoding='utf-8')
if f'- id: {post_id}\n' in arc:
    raise SystemExit(f'{post_id} 已存在於 archive')
published_at = datetime.now(timezone.utc).isoformat()
block = f"""\n- id: {post_id}\n  character: momo\n  date: '2026-09-01'\n  platforms:\n  - instagram\n  caption: 早安！☀️ 九月的第一天，願我們把新的期待放進日常。🐾 慢慢累積的小小努力，終有一天會變成讓自己驕傲的光。今天也要相信自己！✨\n  hashtags:\n  - 默默\n  - 心靈雞湯\n  - 九月你好\n  - 相信自己\n  - ShibaInu\n  media:\n  - content/momo/momo_day01_taipei101.jpg\n  status: published\n  scheduled_time: 07:00\n  published_at: '{published_at}'\n  permalink: {permalink}\n"""
arc_path.write_text(arc.rstrip() + block, encoding='utf-8')
print(f'archived {post_id}: {permalink}')
