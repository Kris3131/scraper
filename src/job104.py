import requests
import time
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

from config import API_CONFIG
from database import save_jobs, save_job_analysis
from analyze import analyze_jobs_with_ai
def fetch_104_jobs():
    all_jobs = []
    page = 1
    
    while True:
        API_CONFIG['PARAMS']['page'] = page
        response = requests.get(API_CONFIG['URL'], headers=API_CONFIG['HEADERS'], params=API_CONFIG['PARAMS'])
        
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
                    job['link'] ['job']if 'link' in job else 'Not provided'
                )
                for job in jobs
            ]
            print(f"found {len(formatted_jobs)} jobs")
            save_jobs(formatted_jobs)

        if OPENAI_API_KEY:
            job_analysis = analyze_jobs_with_ai(jobs)
            save_job_analysis(job_analysis)

        print("update done!")

    except Exception as e:
        print(f"update error: {str(e)}")
