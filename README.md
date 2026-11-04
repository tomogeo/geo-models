# 地理模型教室 原始檔

這個資料夾是「地理模型教室」網站的正本。

- 要新增或更新模型：把 HTML 放進 models/，再請 Claude Code「把新模型加進網站」。
- 模型共同規格、說明卡格式、完整流程：請看 CLAUDE.md。
- index.html：線上版首頁（GitHub Pages）。
- geo-models.html：離線單檔版，雙擊就能用瀏覽器打開，教室沒網路也能用。
- 改完模型後執行 `python3 build.py` 重新產生上面兩個檔。
- 字型：vendor/fonts/ 是網站自帶的思源黑體／宋體（只含用到的字）。新模型出現新字時，build.py 會提醒執行 `python3 fonts.py` 更新。
- 資安：每頁都有「不讓搜尋引擎收錄」與「只准載入網站自己的程式」標記；build.py 會檢查，缺了會停下來提醒；也會檢查有沒有不小心放進金鑰、密碼或外部程式。發現資安問題的通報方式見 SECURITY.md。
