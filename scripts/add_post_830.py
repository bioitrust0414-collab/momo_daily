from pathlib import Path
import yaml

calendar_path = Path('/home/ubuntu/momo_daily_latest/schedule/content-calendar.yaml')
media = 'content/momo/momo_day03_park.jpg'
post = {
    'id': 'momo-20260830',
    'character': 'momo',
    'date': '2026-08-30',
    'platforms': ['instagram'],
    'caption': '早安！☀️ 週日的陽光，提醒我把腳步放慢一點。🐾 給自己一段安靜的時間，整理心情、累積力量，帶著溫柔又堅定的心迎接新的一週吧！✨',
    'hashtags': ['默默', '心靈雞湯', '週日愉快', '慢生活', 'ShibaInu'],
    'media': [media],
    'status': 'ready',
    'scheduled_time': '07:00',
}

with calendar_path.open(encoding='utf-8') as f:
    calendar = yaml.safe_load(f) or []
if isinstance(calendar, dict) and isinstance(calendar.get('posts'), list):
    posts = calendar['posts']
elif isinstance(calendar, list):
    posts = calendar
else:
    raise SystemExit('content-calendar.yaml 格式不是預期的 posts 清單')
if any(p.get('id') == post['id'] for p in posts):
    raise SystemExit(f"{post['id']} 已存在，停止避免重複")
if not (calendar_path.parent.parent / media).exists():
    raise SystemExit(f'素材不存在：{media}')
posts.append(post)
with calendar_path.open('w', encoding='utf-8') as f:
    yaml.safe_dump(calendar, f, allow_unicode=True, sort_keys=False)
print(f"已加入 {post['id']}，狀態為 ready，素材為 {media}")
