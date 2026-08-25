from pathlib import Path
from collections import Counter
import yaml

root = Path('/home/ubuntu/momo_daily_latest')
paths = {}
for folder in ['content', 'reference']:
    for path in (root / folder).rglob('*'):
        if path.is_file() and path.suffix.lower() in {'.jpg', '.jpeg', '.png', '.webp'}:
            paths[str(path.relative_to(root))] = path.stat().st_size

print(f'TOTAL_IMAGE_FILES={len(paths)}')
print(f'TOTAL_IMAGE_BYTES={sum(paths.values())}')
for filename in ['schedule/archive.yaml', 'schedule/content-calendar.yaml']:
    with (root / filename).open(encoding='utf-8') as f:
        data = yaml.safe_load(f) or {}
    refs = []
    for post in data.get('posts', []):
        for media in post.get('media', []) or []:
            if Path(media).suffix.lower() in {'.jpg', '.jpeg', '.png', '.webp'}:
                refs.append((post.get('id'), media))
    print(f'FILE={filename} IMAGE_REFERENCES={len(refs)}')
    for post_id, media in refs:
        size = paths.get(media)
        print(f'REF | {post_id} | {media} | ' + (f'{size} bytes | EXISTS' if size is not None else 'MISSING'))

counts = Counter(media for filename in ['schedule/archive.yaml', 'schedule/content-calendar.yaml'] for post in (yaml.safe_load((root / filename).open(encoding='utf-8')) or {}).get('posts', []) for media in (post.get('media', []) or []) if Path(media).suffix.lower() in {'.jpg', '.jpeg', '.png', '.webp'})
print('DUPLICATE_REFERENCES')
for media, count in sorted(counts.items()):
    if count > 1:
        print(f'{count} | {media}')
