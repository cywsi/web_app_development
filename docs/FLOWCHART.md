# 流程圖文件 (Flowchart) - 活動報名系統

本文檔依據 `docs/PRD.md` 的功能需求與 `docs/ARCHITECTURE.md` 的架構設計，將系統操作邏輯與資料流轉換為視覺化流程圖，以便後續的開發與除錯。

## 1. 使用者流程圖（User Flow）

此流程圖描述「活動創辦者」與「報名者」進入系統後的主要操作路徑與分支條件。

```mermaid
flowchart LR
    Start([使用者開啟網頁]) --> Home[首頁 - 活動列表]
    Home --> Action{要執行什麼操作？}
    
    %% 活動創辦者流程 %%
    Action -->|新增活動| CreateForm[進入建立活動頁面]
    CreateForm --> FillEventInfo[填寫：名稱、簡述、時間表、人數上限]
    FillEventInfo -->|送出表單| SaveEvent[系統儲存活動]
    SaveEvent -->|重導向| EventDetail
    
    %% 報名者/檢視者流程 %%
    Action -->|檢視活動| EventDetail[進入活動詳情頁面]
    EventDetail --> CheckCapacity{報名人數是否已滿？}
    CheckCapacity -->|未滿| ShowForm[顯示報名表單]
    CheckCapacity -->|已滿| DisableForm[顯示「已額滿」，隱藏報名按鈕]
    
    ShowForm --> FillUserInfo[填寫聯絡資訊]
    FillUserInfo -->|送出表單| ProcessRegistration[系統處理報名]
    ProcessRegistration --> Success[報名成功頁面/提示]
```

## 2. 系統序列圖（Sequence Diagram）

此序列圖詳細描述報名者「送出報名表單」直到「資料存入資料庫」的完整過程。為了確保不超賣，這個階段會包含名額的檢查。

```mermaid
sequenceDiagram
    actor User as 報名者
    participant Browser as 瀏覽器
    participant Flask as Flask Route (Controller)
    participant Model as Model (資料庫邏輯)
    participant DB as SQLite database

    User->>Browser: 在活動頁面填寫報名資訊並點選送出
    Browser->>Flask: POST /events/1/register (提交表單資料)
    
    Flask->>Model: 呼叫註冊方法 (event_id, user_info)
    Model->>DB: 開啟 Transaction (交易)
    Model->>DB: SELECT 確認目前活動報名人數與上限
    DB-->>Model: 回傳報名人數 (booked) 與上限 (capacity)
    
    alt 報名人數 < 上限 (未滿)
        Model->>DB: INSERT INTO registrations (寫入報名資料)
        DB-->>Model: 寫入成功
        Model->>DB: Commit Transaction
        Model-->>Flask: 回傳註冊成功
        Flask-->>Browser: HTTP 302 重導向至成功頁面 (或原頁顯示成功提示)
        Browser-->>User: 顯示報名成功訊息
    else 報名人數 >= 上限 (已滿)
        Model->>DB: Rollback Transaction (放棄操作)
        Model-->>Flask: 拋出例外或回傳錯誤 (已額滿)
        Flask-->>Browser: 回傳錯誤訊息頁面
        Browser-->>User: 顯示「很抱歉，活動名額已滿」
    end
```

## 3. 功能清單與路徑對照表

根據上述流程，將功能整理成對應的 URL 路由（URL Route）與 HTTP 方法（HTTP Method）：

| 功能名稱 | 對應路徑 (URL) | HTTP 方法 | 說明 |
| --- | --- | --- | --- |
| 瀏覽活動列表 | `/` 或 `/events` | GET | 首頁，列出近期或是系統內所有建立的活動。 |
| 建立活動頁面 | `/events/create` | GET | 顯示填寫「新增活動」的空白表單。 |
| 送出建立活動 | `/events/create` | POST | 接收建立表單的資料並存入資料庫，成功後重導。 |
| 瀏覽活動詳情 | `/events/<id>` | GET | 顯示單一活動內容（含簡述、時間表、目前報名人數），判斷並顯示報名表單。 |
| 送出報名資料 | `/events/<id>/register` | POST | 接收報名者資訊，進行名額檢查後存入資料庫，額滿則拒絕。 |
