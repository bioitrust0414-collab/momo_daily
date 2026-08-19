import yaml
import datetime
import os

CALENDAR_PATH = "/home/ubuntu/momo_daily_latest/schedule/content-calendar.yaml"
ARCHIVE_PATH = "/home/ubuntu/momo_daily_latest/schedule/archive.yaml"

def update():
    with open(CALENDAR_PATH, "r", encoding="utf-8") as f:
        calendar = yaml.safe_load(f) or {"posts": []}
    
    with open(ARCHIVE_PATH, "r", encoding="utf-8") as f:
        archive = yaml.safe_load(f) or {"posts": []}
    
    new_post = {
        "id": "momo-20260820",
        "character": "momo",
        "date": "2026-08-20",
        "platforms": ["instagram"],
        "caption": "早安！☀️ 星期四的早晨，給自己點一杯咖啡的時間。🐾 生活不必總是匆忙，慢下來感受那份香氣與寧靜。願你的今天充滿溫柔的力量，為即將到來的週末做最好的準備！✨",
        "hashtags": ["默默", "心靈雞湯", "週四愉快", "慢生活", "ShibaInu"],
        "media": ["content/momo/momo_day04_cafe.jpg"],
        "status": "published",
        "scheduled_time": "07:00",
        "published_at": datetime.datetime.now().isoformat(),
        "permalink": "https://www.instagram.com/p/DcPU6ISIHhU/"
    }
    
    archive["posts"].append(new_post)
    
    # Remove if it existed in calendar (though it didn't in this case, good practice)
    calendar["posts"] = [p for p in calendar.get("posts", []) if p.get("id") != "momo-20260820"]
    
    with open(CALENDAR_PATH, "w", encoding="utf-8") as f:
        yaml.safe_dump(calendar, f, allow_unicode=True, sort_keys=False)
        
    with open(ARCHIVE_PATH, "w", encoding="utf-8") as f:
        yaml.safe_dump(archive, f, allow_unicode=True, sort_keys=False)
    
    print("Updated calendar and archive.")

if __name__ == "__main__":
    update()
