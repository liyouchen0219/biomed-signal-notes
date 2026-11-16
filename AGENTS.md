# AGENTS.md

## 目的與範圍
以繁體中文整理醫電訊號處理入門筆記，讀者是剛接觸訊號處理的學生。用可手算的教學數字說明觀念，避免把理想條件寫成實驗結果。勿加入病患資料、金鑰、未做過的實驗或臨床結論。

## 檔案與預覽
- notes/*.json 是唯一的內容來源。一個主題一個檔，檔名用小寫英文與連字號，例如 sampling.json。
- build.py 讀取所有筆記，產生首頁與各篇 HTML。修改共用導覽或版面時改這裡。
- docs/assets/site.css 是共用樣式。docs/*.html 由程式產生，請勿直接編輯。
- 本機執行 python build.py 後開啟 docs/index.html，或用 python -m http.server 8000 --directory docs。
- GitHub Pages 使用 main 分支的 /docs。所有本機頁面與資源一律用相對路徑。

## 新增一篇
1. 查閱 notes/sampling.json。新增 JSON 時保留順序與欄位：order（唯一正整數）、category、title、summary、concept、example、pitfall、references。
2. summary 一句話交代讀者會學到什麼。正文依序為核心觀念、手算例子、容易混淆的地方、延伸閱讀。example 要列出數字、單位與計算。references 至少列一項可核對的教材，每項有 title 和 https URL。
3. 欄位使用純文字，公式用 Unicode 或一般數學符號。生成器會處理 HTML 跳脫。標題和來源要能在各自頁面讀懂。
4. 執行 python build.py。首頁依 order 產生連結，新增筆記不用手動更新導航。
5. 開啟新頁，從首頁點入，再點返回首頁。確認手機寬度下可閱讀，核算例題，檢查來源網址。提交 JSON 與所有對應的生成頁面。

## 版面規則
維持深藍底、青綠重點色與共用字級。首頁放主題索引，內頁使用單欄與明確的小標。連結要保有鍵盤焦點，段落不能靠顏色才能理解。使用現有 CSS 與模板，靜態瀏覽不需要 JavaScript、第三方字型或 API。

## 驗收
建置必須成功，重複建置內容須一致。檢查相對連結與行動版，共用結構的調整須同時檢查首頁和既有內頁。
