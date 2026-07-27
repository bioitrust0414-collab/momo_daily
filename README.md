# momo_daily - Manus AI 驅動的 Instagram 心靈雞湯發布系統

**momo_daily** 是一個自動化的 Instagram 內容發布系統，由 Manus AI 驅動，專門為 Momo 角色發布每日問安與心靈雞湯文案。該系統透過讀取 GitHub 倉庫中的內容排程，自動生成勵志文案，並按指定時程發布到 Instagram。

---

## 系統概述

### 核心特性

**自動化發布流程** - Manus AI 定期掃描 GitHub 倉庫，讀取排程表中 `status: ready` 的貼文，自動發布到 Instagram，無需手動干預。

**心靈雞湯風格** - 所有文案均以溫暖、勵志的「心靈雞湯」風格撰寫，開頭包含問安（早安、午安、晚安），內容具有普遍適用性，不涉及特定情境或故事線。

**去重歸檔機制** - 已發布的貼文自動記錄在 `archive.yaml` 中，確保不會重複發布同一張圖片。

**靈活的排程管理** - 使用 YAML 格式管理排程表，支援人工編輯與版本控制，易於調整發布時間與內容。

**26 張圖片 × 52 天計畫** - 系統包含 26 張精選圖片，按每兩天發布一篇的頻率排程，可支援約 52 天（1.7 個月）的持續發布。

---

## 架構設計

### 工作流程

```
┌─────────────────────────────────────────────────────────┐
│  GitHub Repository (bioitrust0414-collab/momo_daily)    │
└──────────────────┬──────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────┐
│  Manus AI 定時任務 (每兩天觸發)                          │
│  - 讀取 schedule/content-calendar.yaml                  │
│  - 找出當天 status=ready 的貼文                         │
└──────────────────┬──────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────┐
│  Meta Graph API (Instagram Business)                    │
│  - 上傳圖片                                             │
│  - 發布文案與標籤                                       │
└──────────────────┬──────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────┐
│  Instagram 帳號 (@momo_daily 或指定帳號)               │
│  - 貼文發布成功                                         │
└──────────────────┬──────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────┐
│  schedule/archive.yaml (去重歸檔)                       │
│  - 記錄發布時間、Instagram media ID、貼文連結          │
└─────────────────────────────────────────────────────────┘
```

### 核心元件

**content/** - 包含待發布的圖片素材，按日期分類存放（`content/momo/YYYY-MM/YYYYMMDD/`）。

**reference/** - 包含參考資料、角色人設圖、樣本貼文等，不被自動化流程掃描，純供人工查閱。

**schedule/content-calendar.yaml** - 待發布排程表，記錄每篇貼文的圖片、文案、標籤、發布日期與狀態。

**schedule/archive.yaml** - 已發布紀錄，自動記錄發布時間、Instagram media ID 與貼文連結，用於去重與追蹤。

**scripts/publish_to_meta.py** - 發布腳本（舊版，已由 Manus AI 取代），可選保留作為備份。

**scripts/scan_new_content.py** - 內容掃描腳本（舊版，已由 Manus AI 取代），可選保留作為備份。

---

## 文件結構

```
momo_daily/
├── README.md                          # 本文件
├── AGENTS.md                          # 協作規則與流程說明（舊版，已更新）
├── content/                           # 待發布素材
│   └── momo/
│       ├── 2026-05/
│       │   └── 20260520/              # 日期資料夾
│       │       ├── momo_20260520_morning.jpg
│       │       ├── momo_20260520_afternoon.jpg
│       │       └── momo_20260520_cat.jpg
│       └── 2026-06/
│           └── 20260618/
│               ├── momo_20260618_morning.jpg
│               ├── momo_20260618_indoor.jpg
│               └── momo_20260618_cat.jpg
├── reference/                         # 參考資料（不被自動化掃描）
│   ├── character-profile/             # 角色人設圖
│   ├── finals/                        # 最終確定的圖片
│   ├── sample-week/                   # 樣本週貼文
│   ├── templates/                     # 模板
│   ├── momo_character_plan.docx       # 角色企劃書
│   └── momo_content_calendar_30day.docx
├── schedule/                          # 排程與歸檔
│   ├── content-calendar.yaml          # 待發布排程表
│   └── archive.yaml                   # 已發布紀錄
├── scripts/                           # 發布腳本（舊版，已由 Manus AI 取代）
│   ├── publish_to_meta.py
│   └── scan_new_content.py
└── .github/
    └── workflows/                     # GitHub Actions（已停用，改用 Manus AI）
        ├── detect-new-content.yml
        └── publish.yml
```

---

## 排程表格式

### content-calendar.yaml 結構

排程表使用 YAML 格式，每篇貼文包含以下欄位：

| 欄位 | 類型 | 說明 | 範例 |
| --- | --- | --- | --- |
| `id` | string | 唯一識別碼，慣例為 `momo-YYYYMMDD` | `momo-20260727` |
| `character` | string | 角色名稱 | `momo` |
| `date` | string | 預定發布日期（ISO 8601 格式） | `2026-07-27` |
| `platforms` | array | 發布平台清單 | `[instagram]` |
| `caption` | string | 貼文文案（心靈雞湯風格） | `早安！每一天都是新的開始...` |
| `hashtags` | array | 標籤清單 | `["#早安", "#正能量", "#momo"]` |
| `media` | array | 圖片相對路徑清單 | `["content/momo/2026-07/20260727/momo_20260727_morning.jpg"]` |
| `status` | string | 貼文狀態 | `draft` / `ready` / `published` |
| `scheduled_time` | string | 預定發布時間（供參考） | `08:00` |

**狀態說明**:

- `draft` - 草稿，文案尚未完成或待審核

- `ready` - 就緒，可自動發布

- `published` - 已發布（自動設置，發布後移至 archive.yaml）

- `failed` - 發布失敗，需人工檢查與修復

### archive.yaml 結構

已發布紀錄使用統一的 `posts` 陣列，每篇已發布貼文包含：

| 欄位 | 說明 |
| --- | --- |
| `id` | 唯一識別碼 |
| `character` | 角色名稱 |
| `date` | 發布日期 |
| `platforms` | 發布平台 |
| `caption` | 貼文文案 |
| `hashtags` | 標籤清單 |
| `media` | 圖片路徑清單 |
| `status` | 狀態（`published`） |
| `published_at` | 發布時間戳（ISO 8601） |
| `ig_media_id` | Instagram media ID（用於追蹤） |
| `permalink` | Instagram 貼文連結 |

---

## 使用指南

### 1. 新增圖片素材

將新圖片放入 `content/momo/YYYY-MM/YYYYMMDD/` 資料夾中，命名規則為 `momo_YYYYMMDD_描述.jpg`（例如 `momo_20260727_morning.jpg`）。

### 2. 生成文案與排程

Manus AI 會定期掃描新圖片，為每張圖片生成心靈雞湯文案，並在 `content-calendar.yaml` 中建立 `status: draft` 的項目。

**手動編輯排程表**:

```yaml
posts:
  - id: momo-20260727
    character: momo
    date: 2026-07-27
    platforms: [instagram]
    caption: "早安！每一天都是新的開始。無論昨天發生了什麼，今天我們都有機會重新開始，追尋更好的自己。✨"
    hashtags: ["#早安", "#正能量", "#新開始", "#momo"]
    media:
      - content/momo/2026-07/20260727/momo_20260727_morning.jpg
    status: ready
    scheduled_time: "08:00"
```

將 `status` 改為 `ready` 後，Manus AI 會在指定日期自動發布。

### 3. 定時發布

Manus AI 排程任務每兩天自動觸發一次，檢查當天是否有 `status: ready` 的貼文。若有，則透過 Meta Graph API 發布到 Instagram，成功後自動移至 `archive.yaml`。

### 4. 查看已發布紀錄

所有已發布的貼文會自動記錄在 `schedule/archive.yaml` 中，包含發布時間、Instagram 連結與 media ID。

---

## 配置與認證

### 環境變數

Manus AI 排程任務需要以下環境變數，用於連接 Meta Graph API：

| 變數 | 說明 | 取得方式 |
| --- | --- | --- |
| `META_PAGE_TOKEN` | Meta Graph API 的長效 Page/IG Access Token | [Meta for Developers](https://developers.facebook.com/) |
| `IG_USER_ID` | Instagram Business 帳號的 user id | Meta Business Suite 或 Graph API |

**取得 Token 的步驟**:

1. 前往 [Meta for Developers](https://developers.facebook.com/)

1. 建立或選擇應用程式

1. 在「設定」→「基本設定」中找到 Page/IG Access Token

1. 複製 Token 並保存在安全的地方

**設定 Manus AI 排程任務**:

使用 `manus-config` 指令設定排程任務時，將 Token 與 user id 作為環境變數傳入：

```bash
manus-config schedule create \
  --title "momo_daily 定時發布" \
  --detail "讀取 GitHub 倉庫中的排程表，發布 status=ready 的貼文到 Instagram。" \
  --cron "0 0 */2 * * *" \
  --repeated \
  --connector-uids <github-connector-uid>
```

---

## 心靈雞湯文案指南

所有文案應遵循以下原則：

**開頭必須包含問安** - 使用「早安」、「午安」、「晚安」或其他適當的問候語開頭，營造親切感。

**正能量與勵志** - 文案應充滿溫暖、鼓勵與希望，幫助讀者面對每一天的挑戰。

**普遍適用性** - 避免涉及特定情境、故事線或個人經歷，確保文案對所有讀者都有意義。

**簡潔有力** - 文案長度控制在 150-300 字之間，易於在 Instagram 上閱讀。

**搭配標籤** - 每篇文案配 3-5 個相關標籤，如 `#早安`, `#正能量`, `#momo` 等。

**範例文案**:

> 早安！✨ 有時候，我們會被生活中的小挫折打敗，但請記住——每一次跌倒都是站起來的機會。今天，讓我們帶著感謝的心，擁抱新的可能性。你已經比昨天的自己更強大了。💪

---

## 去重與歸檔機制

### 為什麼需要去重？

由於系統支援多種圖片來源（content/ 與 reference/），以及人工編輯排程表的靈活性，必須確保同一張圖片不會被發布多次。

### 去重邏輯

**檔案路徑追蹤** - 系統透過比較 `content-calendar.yaml` 與 `archive.yaml` 中的 `media` 欄位，識別已發布的圖片。

**自動歸檔** - 發布成功後，貼文會自動從 `content-calendar.yaml` 移至 `archive.yaml`，並記錄發布時間、Instagram media ID 與貼文連結。

**人工審核** - 若需要重新發布已發布的貼文，可手動編輯 `archive.yaml`，將項目移回 `content-calendar.yaml` 並改為 `status: ready`。

### 歸檔檔案結構

```yaml
posts:
  - id: momo-20260727
    character: momo
    date: '2026-07-27'
    platforms: [instagram]
    caption: "早安！每一天都是新的開始..."
    hashtags: ["#早安", "#正能量", "#momo"]
    media:
      - content/momo/2026-07/20260727/momo_20260727_morning.jpg
    status: published
    published_at: '2026-07-27T08:00:00.000000'
    ig_media_id: "123456789"
    permalink: "https://www.instagram.com/p/DbHO7e6kYb2/"
```

---

## 故障排除

### 發布失敗

**症狀**: 排程任務執行但貼文未出現在 Instagram 上 。

**可能原因**:

- Meta Graph API Token 過期或無效

- 網路連線中斷

- Instagram 帳號權限不足

- 圖片檔案損壞或無法存取

**解決方案**:

1. 檢查 Manus AI 任務日誌，查看具體錯誤訊息

1. 驗證 `META_PAGE_TOKEN` 是否有效（前往 Meta for Developers 重新授權）

1. 確認 `IG_USER_ID` 正確

1. 檢查 `media` 路徑是否存在且檔案完整

1. 若問題持續，手動檢查 Instagram 帳號是否有限制或警告

### 文案未生成

**症狀**: 新圖片已上傳，但 `content-calendar.yaml` 中沒有新項目。

**可能原因**:

- Manus AI 掃描任務未執行

- 圖片路徑不符合命名規則

- 圖片已在 `archive.yaml` 中（被識別為已發布）

**解決方案**:

1. 確認圖片路徑符合 `content/momo/YYYY-MM/YYYYMMDD/momo_YYYYMMDD_描述.jpg` 格式

1. 手動觸發 Manus AI 掃描任務

1. 檢查 `archive.yaml` 是否已包含該圖片

### Token 過期

**症狀**: 發布失敗，錯誤訊息顯示 `401 Unauthorized`。

**解決方案**:

1. 前往 [Meta for Developers](https://developers.facebook.com/)

1. 選擇應用程式 → 設定 → 基本設定

1. 複製新的 Page/IG Access Token

1. 更新 Manus AI 排程任務的環境變數

1. 手動觸發任務測試新 Token

---

## 發布計畫

### 26 張圖片 × 52 天排程

系統包含 26 張精選圖片，按每兩天發布一篇的頻率排程，可支援約 52 天（1.7 個月）的持續發布。

**圖片來源分佈**:

| 來源 | 數量 | 說明 |
| --- | --- | --- |
| `content/` | 6 張 | 待發布的新素材 |
| `reference/character-profile/` | 5 張 | 角色人設圖 |
| `reference/finals/` | 2 張 | 最終確定的圖片 |
| `reference/sample-week/` | 7 張 | 樣本週貼文 |
| `reference/templates/weekday/` | 6 張 | 每週模板 |
| **總計** | **26 張** | **52 天發布計畫** |

**排程時間表**:

| 週期 | 發布日期 | 貼文數 | 說明 |
| --- | --- | --- | --- |
| 第 1 週 | 2026-07-27, 2026-07-29 | 2 篇 | 啟動階段 |
| 第 2-3 週 | 2026-07-31 - 2026-08-12 | 6 篇 | 穩定發布 |
| 第 4-7 週 | 2026-08-14 - 2026-09-09 | 12 篇 | 持續發布 |
| 第 8-9 週 | 2026-09-11 - 2026-09-24 | 6 篇 | 收尾階段 |

---

## 維護與更新

### 定期檢查

**每週** - 檢查 `archive.yaml` 中的發布紀錄，確保貼文成功發布到 Instagram。

**每月** - 審視文案品質，確保符合心靈雞湯風格與品牌調性。

**定期** - 驗證 Meta Graph API Token 有效性，確保發布流程暢通。

### 新增圖片

若要在現有 52 天計畫之外新增圖片，只需將圖片上傳至 `content/momo/YYYY-MM/YYYYMMDD/` 資料夾，Manus AI 會自動掃描並生成文案。

### 調整排程

若需要調整發布時間或頻率，直接編輯 `content-calendar.yaml` 中的 `date` 與 `scheduled_time` 欄位，或透過 `manus-config schedule update` 指令修改 Manus AI 排程任務。

---

## 技術細節

### 使用的技術棧

- **GitHub** - 版本控制與內容存儲

- **Manus AI** - 自動化發布與文案生成

- **Meta Graph API** - Instagram 發布介面

- **YAML** - 排程表與歸檔格式

### API 整合

系統透過 Meta Graph API 的以下端點進行發布：

- `POST /v20.0/{ig-user-id}/media` - 建立媒體容器

- `POST /v20.0/{ig-user-id}/media_publish` - 發布媒體

詳細文件請參考 [Meta Graph API 官方文件](https://developers.facebook.com/docs/instagram-api)。

### 舊版腳本

`scripts/` 資料夾中的 `publish_to_meta.py` 與 `scan_new_content.py` 是舊版本，已由 Manus AI 取代。保留作為備份與參考，不再主動使用。

---

## 常見問題

**Q: 如果我想暫停發布怎麼辦？**

A: 將所有待發布貼文的 `status` 改為 `draft`，或透過 `manus-config schedule update --enabled=false` 暫停 Manus AI 排程任務。

**Q: 可以一次發布多張圖片嗎？**

A: 目前系統設計為每篇貼文一張圖片。若要發布輪播或影片，需要擴充 Meta Graph API 的容器邏輯（carousel / video container）。

**Q: 文案可以由人工撰寫嗎？**

A: 可以。在 `content-calendar.yaml` 中手動填入 `caption` 與 `hashtags` 欄位，Manus AI 會使用您提供的文案而非自動生成。

**Q: 如何追蹤發布效果？**

A: 所有已發布貼文的 Instagram 連結都記錄在 `archive.yaml` 的 `permalink` 欄位中，可直接點擊查看貼文與互動數據。

**Q: 可以改變發布頻率嗎？**

A: 可以。編輯 `content-calendar.yaml` 中的 `date` 欄位調整發布日期，或透過 `manus-config schedule update --cron` 修改 Manus AI 的觸發頻率。

---

## 聯絡與支援

如有任何問題或建議，請透過以下方式聯絡：

- **GitHub Issues** - 在倉庫中提交 Issue

- **GitHub Discussions** - 在倉庫中開啟討論

- **Manus AI** - 透過 Manus 平台提交反饋

---

## 授權與歸屬

**momo_daily** 由 bioitrust0414-collab 團隊開發與維護，由 Manus AI 提供自動化與文案生成支援。

**圖片素材** - 所有圖片素材為 Momo 角色的官方資產，版權歸原作者所有。

**文案** - 由 Manus AI 自動生成的心靈雞湯文案遵循 Creative Commons 授權，可自由使用與修改。

---

**最後更新**: 2026 年 7 月 27 日**維護者**: Manus AI**倉庫**: [bioitrust0414-collab/momo_daily](https://github.com/bioitrust0414-collab/momo_daily)
