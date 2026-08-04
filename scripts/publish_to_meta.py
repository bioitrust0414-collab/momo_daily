"""
每日發布腳本。
由 .github/workflows/publish.yml 排程呼叫。
流程：
1. 讀 schedule/content-calendar.yaml，找出 date == 今天 且 status == "ready" 的貼文
2. 透過 Meta Graph API 發布到 Instagram
3. 成功後，把該筆從 content-calendar.yaml 移除，加進 schedule/archive.yaml（附發布時間與 media id）
4. 若找不到符合條件的貼文，或呼叫失敗，會印出訊息並以非 0 結束碼結束（方便在 Actions 上看到失敗）

需要的環境變數：
- META_PAGE_TOKEN：長效 Page/IG Access Token
- IG_USER_ID：Instagram Business 帳號的 user id
"""
import os
import sys
import datetime
import traceback
import yaml
import requests

REPO_RAW_BASE = "https://raw.githubusercontent.com/bioitrust0414-collab/momo_daily/main/"
CALENDAR_PATH = "schedule/content-calendar.yaml"
ARCHIVE_PATH = "schedule/archive.yaml"
GRAPH_API_VERSION = "v20.0"


def load_yaml(path, default):
    if not os.path.exists(path):
        print(f"[warn] 找不到 {path}，使用預設值")
        return default
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
        return data if data else default


def save_yaml(path, data):
    with open(path, "w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False)


def find_todays_post(calendar):
    today = datetime.date.today().isoformat()
    posts = calendar.get("posts", [])
    print(f"[info] 今天日期：{today}，calendar 中共有 {len(posts)} 筆貼文")
    for post in posts:
        if post.get("date") == today and post.get("status") == "ready":
            return post
    # 額外印出今天日期有出現、但狀態不是 ready 的項目，方便判斷是不是狀態沒設對
    same_day = [p for p in posts if p.get("date") == today]
    if same_day:
        print(f"[info] 今天有 {len(same_day)} 筆貼文但狀態不是 ready："
              f"{[(p.get('id'), p.get('status')) for p in same_day]}")
    return None


def verify_token(token, ig_user_id):
    """在真正發布前，先確認 token 是否還有效，並印出明確原因。"""
    resp = requests.get(
        f"https://graph.facebook.com/{GRAPH_API_VERSION}/{ig_user_id}",
        params={"fields": "id,username", "access_token": token},
        timeout=30,
    )
    if resp.status_code != 200:
        print(f"[error] Token / IG_USER_ID 驗證失敗，HTTP {resp.status_code}")
        print(f"[error] 回應內容：{resp.text}")
        return False
    print(f"[info] Token 驗證成功，帳號：{resp.json()}")
    return True


def publish_single_image(post, token, ig_user_id):
    """單張圖片發布。多圖輪播 / 影片（Reels）需要不同的 container 流程，
    目前先支援單張圖片，之後可依 media 長度擴充。"""
    if not post.get("media"):
        raise ValueError(f"貼文 {post.get('id')} 沒有 media 欄位，無法發布")

    image_url = REPO_RAW_BASE + post["media"][0]
    caption = post.get("caption", "") + " " + " ".join(post.get("hashtags", []))
    print(f"[info] 準備發布：{post.get('id')}，圖片網址：{image_url}")

    container_resp = requests.post(
        f"https://graph.facebook.com/{GRAPH_API_VERSION}/{ig_user_id}/media",
        data={
            "image_url": image_url,
            "caption": caption.strip(),
            "access_token": token,
        },
        timeout=30,
    )
    if not container_resp.ok:
        print(f"[error] 建立 media container 失敗，HTTP {container_resp.status_code}")
        print(f"[error] 回應內容：{container_resp.text}")
    container_resp.raise_for_status()
    container_id = container_resp.json()["id"]

    publish_resp = requests.post(
        f"https://graph.facebook.com/{GRAPH_API_VERSION}/{ig_user_id}/media_publish",
        data={"creation_id": container_id, "access_token": token},
        timeout=30,
    )
    if not publish_resp.ok:
        print(f"[error] 發布 media 失敗，HTTP {publish_resp.status_code}")
        print(f"[error] 回應內容：{publish_resp.text}")
    publish_resp.raise_for_status()
    return publish_resp.json()


def main():
    token = os.environ.get("META_PAGE_TOKEN")
    ig_user_id = os.environ.get("IG_USER_ID")
    if not token or not ig_user_id:
        missing = []
        if not token:
            missing.append("META_PAGE_TOKEN")
        if not ig_user_id:
            missing.append("IG_USER_ID")
        print(f"[error] 缺少環境變數：{', '.join(missing)}"
              "（請確認 repo Secrets 有設定，且 publish.yml 的 env: 有正確傳入）")
        sys.exit(1)

    calendar = load_yaml(CALENDAR_PATH, {"posts": []})
    archive = load_yaml(ARCHIVE_PATH, {"posts": []})

    post = find_todays_post(calendar)
    if not post:
        print("[info] 今天沒有 status=ready 的貼文，略過。")
        return

    if not verify_token(token, ig_user_id):
        post["status"] = "failed"
        post["notes"] = "token/IG_USER_ID 驗證失敗，請檢查 token 是否過期"
        save_yaml(CALENDAR_PATH, calendar)
        sys.exit(1)

    try:
        result = publish_single_image(post, token, ig_user_id)
    except requests.HTTPError as e:
        print(f"[error] 發布失敗（HTTPError）：{e}")
        post["status"] = "failed"
        post["notes"] = str(e)
        save_yaml(CALENDAR_PATH, calendar)
        sys.exit(1)
    except Exception as e:
        # 捕捉非預期例外（YAML 壞掉、KeyError、網路逾時等），
        # 印出完整 traceback，避免以後又只看到「exit code 1」不知道原因
        print(f"[error] 發布過程發生未預期例外：{e}")
        traceback.print_exc()
        post["status"] = "failed"
        post["notes"] = f"未預期例外：{e}"
        save_yaml(CALENDAR_PATH, calendar)
        sys.exit(1)

    # 歸檔：從待發布移除，附上發布資訊後加進 archive
    calendar["posts"] = [p for p in calendar["posts"] if p is not post]
    post["status"] = "published"
    post["published_at"] = datetime.datetime.now().isoformat()
    post["ig_media_id"] = result.get("id")
    archive.setdefault("posts", []).append(post)
    save_yaml(CALENDAR_PATH, calendar)
    save_yaml(ARCHIVE_PATH, archive)
    print(f"[info] 發布成功並已歸檔：{post['id']}")


if __name__ == "__main__":
    main()
