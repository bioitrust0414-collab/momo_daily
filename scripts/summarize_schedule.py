from pathlib import Path
import yaml

root = Path('/home/ubuntu/momo_daily_latest/schedule')
for filename in ['archive.yaml', 'content-calendar.yaml']:
    path = root / filename
    with path.open(encoding='utf-8') as f:
        data = yaml.safe_load(f) or {}
    posts = data.get('posts', [])
    print(f'FILE={filename}')
    print(f'TOTAL={len(posts)}')
    for post in posts:
        print(' | '.join([
            str(post.get('id', '')),
            str(post.get('date', '')),
            str(post.get('scheduled_time', '')),
            str(post.get('status', '')),
            str(post.get('permalink', '')),
            ','.join(post.get('media', []) or []),
        ]))
