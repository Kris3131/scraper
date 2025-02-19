# 104 Remote Jobs Scraper

這是一個自動化爬取 104 人力銀行遠端工作職缺的專案，並使用 OpenAI GPT API 分析職缺所需技能。

## 功能特點

- 自動爬取 104 人力銀行遠端工作職缺
- 使用 OpenAI GPT 分析職缺描述，提取所需技能
- 資料存儲於 SQLite 資料庫
- 支援 Docker 容器化部署
- 非同步處理，提高效能

## 環境需求

- Python 3.9+
- Docker (選用)

## 安裝方式

### 1. 複製專案

```sh
git clone git@github.com:Kris3131/scraper.git
cd scraper

2. 建立環境變數檔案

cp .env.example .env

編輯 .env 檔案，加入你的 OpenAI API Key：

OPENAI_API_KEY=your-api-key-here

3. 運行專案

選擇以下其中一種方式運行：

使用 Python 虛擬環境

python -m venv venv
source venv/bin/activate  # Linux/Mac

pip install -r requirements.txt
python src/scraper.py

使用 Docker

docker-compose up --build

專案結構

.
├── src/
│   ├── analyze.py      # OpenAI API 職缺分析
│   ├── config.py       # 設定檔
│   ├── database.py     # 資料庫操作
│   ├── job104.py       # 104 爬蟲主程式
│   └── scraper.py      # 程式進入點
├── data/               # 資料庫存放位置
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md

資料庫結構

jobs Table

Column Name	Type	Description
id	INTEGER	Primary key
job_id	TEXT	Job ID
title	TEXT	Job Title
company	TEXT	Company Name
salary	TEXT	Salary Range
job_description	TEXT	Job Description
link	TEXT	Job Link
is_applied	BOOLEAN	Is Applied
timestamp	DATETIME	Create Time

job_analysis Table

Column Name	Type	Description
job_id	TEXT	Job ID (Foreign key)
skills	TEXT	Skills extracted by GPT

```

未來優化方向

- 重構( config / logger / database / job104 / analyze)
- 錯誤處理與日誌記錄(logger 模組，取代現有的 print)
- 多環境設定(dev, prod)
- 單元測試

功能優化方向

- 通知 (line)
- 自動化排程
- 上傳履歷，自動產出 cover letter
