import asyncio
import aiohttp
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

from config import API_CONFIG
from database import save_jobs, save_job_analysis
from analyze import analyze_jobs_with_ai

async def fetch_page(session, page):
    API_CONFIG['PARAMS']['page'] = page
    try:
        async with session.get(API_CONFIG['URL'], 
                             headers=API_CONFIG['HEADERS'], 
                             params=API_CONFIG['PARAMS']) as response:
            if response.status != 200:
                print(f"104 page {page} jobs fetch failed! Status code: {response.status}")
                return []
            jobs_data = await response.json()
            jobs = jobs_data.get('data', [])
            print(f"104 page {page} jobs fetched, {len(jobs)} jobs")
            return jobs
    except Exception as e:
        print(f"Error fetching page {page}: {str(e)}")
        return []

async def fetch_104_jobs():
    all_jobs = []
    async with aiohttp.ClientSession() as session:
        page = 1
        while True:
            jobs = await fetch_page(session, page)
            if not jobs:
                break
            all_jobs.extend(jobs)
            page += 1
            await asyncio.sleep(1)  # 保留延遲以避免被封鎖
    
    print(f"104 total {len(all_jobs)} jobs fetched")
    return all_jobs

async def scrape_and_save():
    """ Main function: fetch and save jobs, then use AI to analyze skills and cover letter """
    try:
        print("\n start updating jobs...")
        jobs = await fetch_104_jobs()
        
        if jobs:
            formatted_jobs = [
                (
                    job['jobName'] if 'jobName' in job else 'Not provided',
                    job['custName'] if 'custName' in job else 'Not provided',
                    job['salaryLow'] if 'salaryLow' in job else 'Not provided',
                    job['description'] if 'description' in job else 'Not provided',
                    job['link']['job'] if 'link' in job else 'Not provided'
                )
                for job in jobs
            ]
            print(f"found {len(formatted_jobs)} jobs")
            save_jobs(formatted_jobs)

        if OPENAI_API_KEY:
            job_analysis = await analyze_jobs_with_ai(jobs)
            save_job_analysis(job_analysis)

        print("update done!")

    except Exception as e:
        print(f"update error: {str(e)}")

# 新增執行入口點
if __name__ == "__main__":
    asyncio.run(scrape_and_save())
