# 路由設計文件 (Routes Design)

依照系統架構 (`docs/ARCHITECTURE.md`) 與流程圖 (`docs/FLOWCHART.md`)，本系統設計了以下路由與對應模板，以提供「活動建立」與「活動報名」兩大核心功能。

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| --- | --- | --- | --- | --- |
| 首頁 (活動列表) | GET | `/` | `index.html` | 顯示所有活動列表 |
| 建立活動頁面 | GET | `/events/create` | `create.html` | 顯示新增活動的表單 |
| 建立活動 | POST | `/events/create` | — | 接收表單並寫入 DB，重導至首頁或詳情頁 |
| 活動詳情頁面 | GET | `/events/<int:id>` | `detail.html` | 顯示活動資訊與報名表單 |
| 送出報名 | POST | `/events/<int:id>/register` | — | 寫入報名資料，處理滿額檢查，若成功重導回詳情頁 |

## 2. 每個路由的詳細說明

### 首頁 (活動列表)
- **輸入**: 無
- **處理邏輯**: 呼叫 `EventModel.get_all()` 取得包含報名數與容量的活動清單。
- **輸出**: 渲染 `index.html`，將 `events` 資料傳遞給模板呈現。

### 建立活動頁面
- **輸入**: 無
- **處理邏輯**: 準備顯示空白的活動建立表單。
- **輸出**: 渲染 `create.html`。

### 建立活動
- **輸入**: 表單欄位 `title`, `description`, `start_time`, `end_time`, `capacity`
- **處理邏輯**: 
  - 驗證必填欄位 (標題、開始與結束時間、人數上限)。
  - 呼叫 `EventModel.create(...)` 將活動存入資料庫。
- **輸出**: 建立成功後使用 Flash Message 提示，並重導向 (Redirect) 至該活動的詳情頁或首頁。
- **錯誤處理**: 如果資料不齊全，回傳 `create.html` 並帶有錯誤提示訊息。

### 活動詳情頁面
- **輸入**: URL 參數 `id` (活動 ID)
- **處理邏輯**: 
  - 呼叫 `EventModel.get_by_id(id)`，包含目前已報名人數。
- **輸出**: 渲染 `detail.html`，並將活動物件 `event` 傳入。
- **錯誤處理**: 如果查無此活動，可回傳 404 頁面或重導回首頁並顯示錯誤。

### 送出報名
- **輸入**: URL 參數 `id`, 表單欄位 `user_name`, `user_email`, `user_phone`
- **處理邏輯**: 
  - 呼叫 `RegistrationModel.create(event_id=id, ...)`。
  - 此 Model 方法內部有 Transaction 可防止超賣。
- **輸出**: 成功時重導至 `detail.html` (原頁面) 並新增「報名成功」的 Flash Message。
- **錯誤處理**: 捕捉滿額或活動不存在的 Exception，若發生錯誤，則設定 Flash 錯誤訊息「很抱歉，活動名額已滿」並重導回 `detail.html` 或顯示錯誤。

## 3. Jinja2 模板清單

所有的模板均位於 `app/templates/`。

| 檔案名稱 | 繼承自 | 用途 |
| --- | --- | --- |
| `base.html` | (無) | 共用的外觀版型，包含 Header、Footer、Flash Message 與匯入靜態資源 (CSS/JS)。 |
| `index.html` | `base.html` | 呈現所有活動的列表清單，包含活動標題、時間、剩餘名額狀態。 |
| `create.html` | `base.html` | 填寫新增活動的表單，包含基本的 HTML5 驗證功能。 |
| `detail.html` | `base.html` | 單一活動的完整介紹。由 Jinja2 判斷：若名額滿則顯示「已額滿」，未滿則渲染出「報名表單區塊」。 |

## 4. 路由骨架程式碼

路由的 Python 骨架程式碼已經建立於 `app/routes/routes.py`。
