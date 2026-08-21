import yaml

CALENDAR_PATH = "/home/ubuntu/momo_daily_latest/schedule/content-calendar.yaml"

def add_post():
    with open(CALENDAR_PATH, "r", encoding="utf-8") as f:
        calendar = yaml.safe_load(f) or {"posts": []}
        
    next_post = {
        "id": "momo-20260822",
        "character": "momo",
        "date": "2026-08-22",
        "platforms": ["instagram"],
        "caption": "早安！☀️ 週六的巷弄漫步，最適合放慢腳步。🐾 生活中的美好往往藏在不經意的轉角處，給自己一個微笑，享受這份專屬於周末的寧靜與悠閒吧！✨",
        "hashtags": ["默默", "心靈雞湯", "週末愉快", "巷弄日常", "ShibaInu"],
        "media": ["content/momo/momo_day08_alley.jpg"],
        "status": "ready",
        "scheduled_time": "07:00"
    }
    
    # Check if already exists
    exists = any(p.get("id") == "momo-20260822" for p in calendar.get("posts", []))
    if not exists:
        calendar["posts"].append(next_post)
        with open(CALENDAR_PATH, "w", encoding="utf-8") as f:
            yaml.safe_dump(calendar, f, allow_unicode=True, sort_keys=False)
        print("Successfully added 2026-08-22 post to calendar.")
    else:
        print("Post 2026-08-22 already exists in calendar.")

if __name__ == "__main__":
    add_post()
