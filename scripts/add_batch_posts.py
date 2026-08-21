import yaml

CALENDAR_PATH = "/home/ubuntu/momo_daily_latest/schedule/content-calendar.yaml"

def add_posts():
    with open(CALENDAR_PATH, "r", encoding="utf-8") as f:
        calendar = yaml.safe_load(f) or {"posts": []}
        
    new_posts = [
        {
            "id": "momo-20260824",
            "character": "momo",
            "date": "2026-08-24",
            "platforms": ["instagram"],
            "caption": "早安！☀️ 新的一週又開始了，給自己一個自信的微笑吧。🐾 無論挑戰有多大，只要步伐堅定，每一步都是向夢想靠近。今天也要元氣滿滿地出發！✨",
            "hashtags": ["默默", "心靈雞湯", "週一加油", "正能量", "ShibaInu"],
            "media": ["content/momo/momo_day09_profile.jpg"],
            "status": "ready",
            "scheduled_time": "07:00"
        },
        {
            "id": "momo-20260826",
            "character": "momo",
            "date": "2026-08-26",
            "platforms": ["instagram"],
            "caption": "早安！☀️ 週三的小步伐，是支撐我們繼續前進的溫柔力量。🐾 聽聽音樂，喝杯溫水，給緊湊的步伐一點喘息的空間。願你的今天平靜而美好！✨",
            "hashtags": ["默默", "心靈雞湯", "週三小確幸", "內心平靜", "ShibaInu"],
            "media": ["content/momo/momo_day10_portrait.jpg"],
            "status": "ready",
            "scheduled_time": "07:00"
        },
        {
            "id": "momo-20260828",
            "character": "momo",
            "date": "2026-08-28",
            "platforms": ["instagram"],
            "caption": "早安！☀️ 迎向星期五的曙光，心裡已經開始期待美好的週末。🐾 把本周的疲憊通通甩掉，用最燦爛的笑容迎接接下來的悠閒時光吧！✨",
            "hashtags": ["默默", "心靈雞湯", "週五愉快", "期待週末", "ShibaInu"],
            "media": ["content/momo/momo_day11_energy.jpg"],
            "status": "ready",
            "scheduled_time": "07:00"
        }
    ]
    
    existing_ids = {p.get("id") for p in calendar.get("posts", [])}
    
    added_count = 0
    for np in new_posts:
        if np["id"] not in existing_ids:
            calendar["posts"].append(np)
            added_count += 1
            
    with open(CALENDAR_PATH, "w", encoding="utf-8") as f:
        yaml.safe_dump(calendar, f, allow_unicode=True, sort_keys=False)
        
    print(f"Successfully added {added_count} new posts to calendar.")

if __name__ == "__main__":
    add_posts()
