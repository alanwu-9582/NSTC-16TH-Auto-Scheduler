NSTC-16TH Auto Scheduler
======

![license MIT](https://img.shields.io/badge/license-MIT-blue)
![python 3.10.6](https://img.shields.io/badge/python-3.10.6-blue)

> 2023 &copy; alanwu-9852

專案簡介
---
這個專案可以協助[南山高中交通服務隊](https://www.instagram.com/nstc_16th/?utm_source=ig_web_button_share_sheet&igshid=ZDNlZDc0MzIxNw==)**偉大的總指揮勤務長大人**排班表。大幅縮減每個月排班表所花的時間

使用說明
---
下載與安裝:
至 [Releases](https://github.com/alanwu-9582/NSTC-S2-Auto-Scheduler/releases) NSTC-16TH Auto Scheduler
解壓縮後執行 main.exe ，如果無法執行請嘗試關閉防毒軟體 :P


開始使用:

* 匯入符合格式的名單與班表模板
* 設定最大值勤次數，與最大早班次數
* 開始排班
* 匯出班表
* 完成!!

使用範例:

1. 啟動程式。
2. 點擊匯入名單匯入[符合格式的名單](data/members.json)
3. 點擊匯入班表模版匯入[符合格式的班表模板](data/schedule.json)
4. 設定最大值勤次數，與最大早班次數
5. 點擊 "開始排班" 按鈕，程式將自動完成排班。
6. 匯出班表可以將班表以 csv 格式匯出，可以用 Excel 開啟

編輯成員:

1.	使用下拉試選單選擇要編輯的成員
2.	點擊 “編輯成員” 即可編輯該成員無法值勤的時間
3.	可使用編輯區下方的功能鍵添加無法值勤條件，也可以直接修改編輯區的內容(手動輸入必須符合格式要求)
4.	編輯完畢後務必點擊 “儲存編輯” 


其他說明:

1.	班表模板與名單須符合格式
2.	目前已支援高一與高二的排班
3.	已經盡可能平均分配工作，但仍有部分需要手動微調


版本更新
---
* v1.0.0 (2023/10/15): 初版
* v1.0.1 (2023/10/18):
    1. 可支援高一與高二的排班
    2. 依照每個人的權重進行班表的分配
    3. 可透過功能按鈕添加無法值勤的條件
	4. 修復了匯入名單後須重新開啟才能生效的問題


待做功能
---
以下是一些待做的功能：

- [ ] 想到要做那些功能

如果你有任何建議或問題，請隨時聯繫作者