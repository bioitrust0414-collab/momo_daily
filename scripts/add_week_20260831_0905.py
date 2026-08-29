from pathlib import Path
import yaml

ROOT = Path('/home/ubuntu/momo_daily_latest')
CALENDAR_PATH = ROOT / 'schedule/content-calendar.yaml'

posts = [
    {
        'id': 'momo-20260831', 'character': 'momo', 'date': '2026-08-31',
        'platforms': ['instagram'],
        'caption': '早安！☀️ 新的一週，先給自己一個肯定的微笑。🐾 不必一次走完所有路，只要踏穩今天的每一步，就已經在靠近想去的地方。星期一也要溫柔出發！✨',
        'hashtags': ['默默', '心靈雞湯', '週一加油', '溫柔出發', 'ShibaInu'],
        'media': ['reference/templates/weekday/momo_morning_mon.jpg'], 'status': 'ready', 'scheduled_time': '07:00'
    },
    {
        'id': 'momo-20260901', 'character': 'momo', 'date': '2026-09-01',
        'platforms': ['instagram'],
        'caption': '早安！☀️ 九月的第一天，願我們把新的期待放進日常。🐾 慢慢累積的小小努力，終有一天會變成讓自己驕傲的光。今天也要相信自己！✨',
        'hashtags': ['默默', '心靈雞湯', '九月你好', '相信自己', 'ShibaInu'],
        'media': ['content/momo/momo_day01_taipei101.jpg'], 'status': 'ready', 'scheduled_time': '07:00'
    },
    {
        'id': 'momo-20260902', 'character': 'momo', 'date': '2026-09-02',
        'platforms': ['instagram'],
        'caption': '早安！☀️ 週三的你，已經比想像中更努力了。🐾 先停下來深呼吸，肯定自己的進度，再帶著平靜的力量繼續前進。✨',
        'hashtags': ['默默', '心靈雞湯', '週三加油', '平靜力量', 'ShibaInu'],
        'media': ['reference/templates/weekday/momo_morning_wed.jpg'], 'status': 'ready', 'scheduled_time': '07:00'
    },
    {
        'id': 'momo-20260903', 'character': 'momo', 'date': '2026-09-03',
        'platforms': ['instagram'],
        'caption': '早安！☀️ 生活的美好，常常藏在一杯溫水、一陣微風和一個被善待的瞬間裡。🐾 今天也記得照顧自己的心，讓日子慢慢發亮。✨',
        'hashtags': ['默默', '心靈雞湯', '日常微光', '溫柔生活', 'ShibaInu'],
        'media': ['reference/templates/weekday/momo_morning_thu.jpg'], 'status': 'ready', 'scheduled_time': '07:00'
    },
    {
        'id': 'momo-20260904', 'character': 'momo', 'date': '2026-09-04',
        'platforms': ['instagram'],
        'caption': '早安！☀️ 星期五到了，謝謝這一週努力沒有放棄的自己。🐾 把疲憊留在昨天，帶著笑容迎接週末，也把一點小小的幸福留給自己。✨',
        'hashtags': ['默默', '心靈雞湯', '週五愉快', '謝謝自己', 'ShibaInu'],
        'media': ['reference/character-profile/momo_profile_01.jpg'], 'status': 'ready', 'scheduled_time': '07:00'
    },
    {
        'id': 'momo-20260905', 'character': 'momo', 'date': '2026-09-05',
        'platforms': ['instagram'],
        'caption': '早安！☀️ 週六就讓步調輕一點吧。🐾 去走一段喜歡的路，看看熟悉風景裡的新發現，願你在簡單的日子裡收集滿滿的自在與安心。✨',
        'hashtags': ['默默', '心靈雞湯', '週六愉快', '慢生活', 'ShibaInu'],
        'media': ['reference/templates/weekday/momo_morning_sat.jpg'], 'status': 'ready', 'scheduled_time': '07:00'
    },
]

with CALENDAR_PATH.open(encoding='utf-8') as f:
    calendar = yaml.safe_load(f) or {'posts': []}
if not isinstance(calendar, dict) or not isinstance(calendar.get('posts'), list):
    raise SystemExit('content-calendar.yaml 格式不是預期的 posts 清單')
existing = {p.get('id') for p in calendar['posts']}
for post in posts:
    if post['id'] in existing:
        raise SystemExit(f"{post['id']} 已存在，停止避免重複")
    if not (ROOT / post['media'][0]).is_file():
        raise SystemExit(f"素材不存在：{post['media'][0]}")
calendar['posts'].extend(posts)
with CALENDAR_PATH.open('w', encoding='utf-8') as f:
    yaml.safe_dump(calendar, f, allow_unicode=True, sort_keys=False)
print('已加入 6 筆排程：' + ', '.join(p['id'] for p in posts))
