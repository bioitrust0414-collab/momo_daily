import yaml
import datetime

CALENDAR_PATH = "/home/ubuntu/momo_daily_latest/schedule/content-calendar.yaml"
ARCHIVE_PATH = "/home/ubuntu/momo_daily_latest/schedule/archive.yaml"

def archive():
    with open(CALENDAR_PATH, "r", encoding="utf-8") as f:
        calendar = yaml.safe_load(f) or {"posts": []}
    
    with open(ARCHIVE_PATH, "r", encoding="utf-8") as f:
        archive = yaml.safe_load(f) or {"posts": []}
    
    post_id = "momo-20260822"
    target_post = None
    
    for p in calendar.get("posts", []):
        if p.get("id") == post_id:
            target_post = p
            break
            
    if target_post:
        target_post["status"] = "published"
        target_post["published_at"] = datetime.datetime.now().isoformat()
        target_post["permalink"] = "https://www.instagram.com/p/DcUfpV3kfxq/"
        
        archive["posts"].append(target_post)
        calendar["posts"] = [p for p in calendar["posts"] if p.get("id") != post_id]
        
        with open(CALENDAR_PATH, "w", encoding="utf-8") as f:
            yaml.safe_dump(calendar, f, allow_unicode=True, sort_keys=False)
        with open(ARCHIVE_PATH, "w", encoding="utf-8") as f:
            yaml.safe_dump(archive, f, allow_unicode=True, sort_keys=False)
        print(f"Archived {post_id}")
    else:
        print(f"Post {post_id} not found in calendar.")

if __name__ == "__main__":
    archive()
