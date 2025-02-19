API_CONFIG = {
    'URL': "https://www.104.com.tw/jobs/search/api/jobs",
    'HEADERS': {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36",
        "Referer": "https://www.104.com.tw/jobs/search/?remoteWork=1",
        "Accept": "application/json"
    },
    'PARAMS': {
        "isJobList": 1,
        "jobcat": "2007001004,2007001016",  # 後端工程師 / 全端工程師
        "jobsource": "joblist_search",
        "order": 15,  # 按照最新更新排序
        "page": 1,  # 第 1 頁
        "pagesize": 20,  # 一次取得 20 筆
        "remoteWork": 1,  # 只抓取遠端職缺
        "searchJobs": 1
    }
}