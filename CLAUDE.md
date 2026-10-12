# 地理模型教室：給 Claude Code 的專案說明

## 專案是什麼
呂世友老師（Tomo，胡志明市臺灣學校地理老師）的互動地理教學模型網站。
首頁依主題（水文、氣候、地形、人文）列出模型，點開即可投影上課。模型會持續增加。
溝通一律用繁體中文、臺灣用字。老師不是工程師：說明時少用術語，需要他操作時一步一步講。

## 工具分工
- Claude Chat（claude.ai 專案「地理課程模型」）：從零做新模型、預覽、反覆修改。
- Claude Code（這裡）：這個資料夾是網站的**唯一正本**。負責加入模型、組裝、測試、發布。
- 模型改版時，老師會把新的 HTML 放進 models/，一律以資料夾裡的檔案為準。

## 資料夾結構（目前）
- models/<id>.html：每個模型一個獨立、可單獨開啟的 HTML
- registry.json：主題與模型清單，含每個模型的說明卡（格式見下）
- template.html：首頁與播放畫面外框
- build.py：把 registry、模型、外框組成單一檔 geo-models.html（模型以 iframe srcdoc 內嵌）
- vendor/three.r128.min.js：3D 元件（three.js r128，MIT 授權見 three.LICENSE），供離線使用
- 舊的線上版網址（需登入 Claude 才能看）：https://claude.ai/artifact/5MoM7QfdsYexHY2Ynz2WKH

## 首次任務（依序做，每步完成向老師回報）
1. 建立 git 版本控制並做第一次提交。
2. 帶老師建立 GitHub 帳號與公開 repo，設定 GitHub Pages，讓學生不用登入就能開網站。
   需要老師本人操作的步驟（註冊、登入、授權）請清楚說明並等他完成，不要代他輸入密碼。
3. 調整成適合 GitHub Pages 的結構：
   - index.html 為首頁；模型改用 iframe src="models/<id>.html" 載入（不再把所有模型塞進一個檔）。
   - 模型裡的 three.js 從 CDN 改為讀 ../vendor/three.r128.min.js，讓 3D 離線也能顯示。
   - build.py 保留並改為另外輸出一份「離線單檔版」geo-models.html（three.js 內嵌），給教室沒網路或隨身碟用。
   - 保留 #<id> 直接開啟某個模型、Esc 回首頁、全螢幕按鈕等現有功能。
4. 首頁卡片或播放畫面加入「說明卡」內容（學習重點、上課操作建議），設計要乾淨、不擋模型。
5. 用瀏覽器實際測試（1366×768 投影尺寸與手機寬度），推上線，把公開網址給老師。

## 規格一：模型共同規格（新模型與改版都要符合）
- 單一 HTML 檔、可獨立開啟；CSS、JS 寫在檔內。外部腳本只准用 vendor/ 內的檔案。
- 必須能在 iframe 內正常運作：不得呼叫 history.pushState / replaceState 或改網址；
  若用 localStorage 一律 try/catch，讀不到也要正常顯示。
- 快捷鍵統一：
  - F：全螢幕
  - R：重來／重播
  - ← →（或空白鍵）：步驟型模型的上一步、下一步
  - 1、2、3…：切換情境或分頁
  - Esc：保留給網站「回首頁」，模型本身不要使用
- 深淺色：用 prefers-color-scheme，並支援 :root[data-theme="light"|"dark"]。
- 投影可讀：以 1366×768 為準，主要內容不需捲動，內文字級至少 16px；手機寬度也要能操作。
- 3D 或任何元件載入失敗時，顯示簡短提示，其餘功能照常可用。
- 模型內註明資料來源與簡化說明（例：「理想化模型，僅供教學示意」）。
- 臺灣用字、繁體中文；地名與專有名詞依課本用法。

## 規格二：模型說明卡（寫在 registry.json 的每個模型裡）
| 欄位 | 內容 |
|---|---|
| id | 英文代號，等於 models/ 裡的檔名 |
| topic | 主題代號：hydro 水文、climate 氣候、landform 地形、human 人文（可新增） |
| icon | 一個 emoji |
| title | 模型名稱 |
| desc | 一兩句說明，顯示在首頁 |
| keys | 上課操作快捷鍵（可含 <kbd>） |
| level | 國中／高中／國中、高中 |
| unit | 對應課本冊別與單元（例：高一上 第3章 河流） |
| goals | 學習重點，2 到 4 點 |
| steps | 上課操作建議，3 到 5 步 |
| source | 資料來源與簡化說明 |

現有四個模型的說明卡是 Claude 依模型內容寫的草稿，unit 目前都是「待填」。
第一次設定完成後，請把四張卡念給老師確認，並請他補上 unit。

## 新增模型的標準流程
1. 老師把新模型 HTML 放進 models/（或提供 claude.ai 連結，請他下載後放入）。
2. 檢查是否符合規格一；不符合的地方先列出來問老師，再修改。
3. 在 registry.json 加一筆，說明卡欄位不清楚的地方問老師，不要自己編 unit。
4. 組裝、在瀏覽器測試（開啟、快捷鍵、Esc 回首頁、手機寬度），提交並推上線。
5. 回報：加了什麼、網址、有沒有需要老師注意的地方。

## 小 Claude 通知站（老師桌面上的置頂提醒）
- 網址：https://claude.ai/artifact/GJyBbCrdMbLotJkQdzgWam （老師在 Chrome 開啟、置頂在桌面）
- 用 ArtifactData 工具寫入 collection `pet`、doc_id `status`：
  `{"state": "working" | "done" | "ask" | "idle", "message": "一句話摘要（30 字內）", "updatedAt": 現在的毫秒時間戳}`
  （先 get 讀出 version，寫入時帶 if_version；取時間可用 `date +%s%3N`）
- 什麼時候寫：
  - 開始一項較長的任務 → `working`
  - 任務完成、等老師看結果 → `done`
  - 需要老師回答問題或親自操作 → `ask`，message 寫問題摘要
