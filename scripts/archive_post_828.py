import datetime
import yaml

CALENDAR_PATH = "/home/ubuntu/momo_daily_latest/schedule/content-calendar.yaml"
ARCHIVE_PATH = "/home/ubuntu/momo_daily_latest/schedule/archive.yaml"
POST_ID = "momo-20260828"
PERMALINK = "https://www.instagram.com/p/DcexQ89oNVw/"

with open(CALENDAR_PATH, encoding="utf-8") as f:
    calendar = yaml.safe_load(f) or {"posts": []}
with open(ARCHIVE_PATH, encoding="utf-8") as f:
    archive = yaml.safe_load(f) or {"posts": []}

post = next((p for p in calendar.get("posts", []) if p.get("id") == POST_ID), None)
if post is None:
    raise SystemExit(f"找不到 {POST_ID}，未修改檔案")

post["status"] = "published"
post["published_at"] = datetime.datetime.now().isoformat()
post["permalink"] = PERMALINK
archive.setdefault("posts", []).append(post)
calendar["posts"] = [p for p in calendar.get("posts", []) if p.get("id") != POST_ID]

with open(CALENDAR_PATH, "w", encoding="utf-8") as f:
    yaml.safe_dump(calendar, f, allow_unicode=True, sort_keys=False)
with open(ARCHIVE_PATH, "w", encoding="utf-8") as f:
    yaml.safe_dump(archive, f, allow_unicode=True, sort_keys=False)
print(f"已歸檔 {POST_ID}: {PERMALINK}")
