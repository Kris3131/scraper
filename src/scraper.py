import requests
import time

from database import init_db, save_jobs

# 104 API 職缺查詢網址
API_URL = "https://www.104.com.tw/jobs/search/api/jobs"
PARAMS = {
    "isJobList": 1,
    "jobcat": "2007001004,2007001016",  # 後端工程師 / 全端工程師
    "jobsource": "joblist_search",
    "order": 15,  # 按照最新更新排序
    "page": 1,  # 第 1 頁
    "pagesize": 20,  # 一次取得 20 筆
    "remoteWork": 1,  # 只抓取遠端職缺
    "searchJobs": 1
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36",
    "Referer": "https://www.104.com.tw/jobs/search/?remoteWork=1",
    "Accept": "application/json"
}

def fetch_104_jobs():
    """ 爬取 104 職缺 API """
    all_jobs = []
    page = 1
    
    while True:
        PARAMS['page'] = page
        response = requests.get(API_URL, headers=HEADERS, params=PARAMS)
        
        if response.status_code != 200:
            print(f"104 {page} page jobs fetch failed! Status code: {response.status_code}")
            break

        jobs_data = response.json()
        jobs = jobs_data.get('data', []) 
        
        # 如果沒有更多職缺，就跳出迴圈
        if not jobs:
            break
            
        all_jobs.extend(jobs)
        print(f"104 {page} page jobs fetched, {len(jobs)} jobs")
        page += 1
        time.sleep(1)
    
    print(f"104 total {len(all_jobs)} jobs fetched")
    return all_jobs

def scrape_and_save():
    """ Main function: fetch and save jobs, then use AI to analyze skills and cover letter """
    try:
        print("\n start updating jobs...")
        jobs = fetch_104_jobs()
        
        if jobs:
            formatted_jobs = [
                (
                    job['jobName'] if 'jobName' in job else 'Not provided',
                    job['custName'] if 'custName' in job else 'Not provided',
                    job['salaryLow'] if 'salaryLow' in job else 'Not provided',
                    job['description'] if 'description' in job else 'Not provided',
                    f"https://www.104.com.tw/job/{job['jobNo'] if 'jobNo' in job else ''}"
                )
                for job in jobs
            ]
            print(f"found {len(formatted_jobs)} jobs")
            save_jobs(formatted_jobs)

        print("update done!")
    except Exception as e:
        print(f"update error: {str(e)}")



def main():
    try: 
        init_db()
        scrape_and_save()
    except KeyboardInterrupt:
        print("KeyboardInterrupt: Exiting gracefully...")
        return
    except Exception as e:
        print(f"Error initializing database: {e}")
        return    

if __name__ == "__main__":
    main()            