import aiohttp
import asyncio
import json
import os
from typing import List, Tuple
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
MAX_CONCURRENT_REQUESTS = 3  # 控制並發請求數量
RATE_LIMIT_DELAY = 3  # OpenAI API 請求間隔（秒）

async def analyze_single_job(session: aiohttp.ClientSession, 
                           job: dict, 
                           semaphore: asyncio.Semaphore) -> Tuple[str, str]:
    job_desc = job.get('description', 'Not provided')
    job_no = job.get('jobNo', 'unknown')
    
    async with semaphore:  # 使用 semaphore 控制並發
        try:
            payload = {
                "model": "gpt-3.5-turbo",
                "messages": [
                    {"role": "system", "content": "你是一個職缺分析助手。請分析職缺描述並返回 JSON 格式的結果，skills（需要的技能列表）"},
                    {"role": "user", "content": f"職缺描述: {job_desc}"}
                ]
            }
            headers = {
                "Authorization": f"Bearer {OPENAI_API_KEY}",
                "Content-Type": "application/json"
            }

            async with session.post("https://api.openai.com/v1/chat/completions", 
                                  json=payload, 
                                  headers=headers) as response:
                if response.status == 200:
                    result = await response.json()
                    ai_content = result["choices"][0]["message"]["content"]
                    print(f"\nJob {job_no} AI response: {ai_content}")

                    ai_response = json.loads(ai_content)
                    skills = json.dumps(ai_response['skills'], ensure_ascii=False)
                    await asyncio.sleep(RATE_LIMIT_DELAY)  # 避免超過 API 限制
                    return job_no, skills
                else:
                    print(f"AI analysis failed for job {job_no}, status code: {response.status}")
                    return job_no, "[]"

        except Exception as e:
            print(f"Error analyzing job {job_no}: {str(e)}")
            return job_no, "[]"

async def analyze_jobs_with_ai(jobs: List[dict]) -> List[Tuple[str, str]]:
    if not OPENAI_API_KEY:
        print("OpenAI API Key not set, skip AI analysis")
        return []

    jobs = jobs[:20]  # 限制處理前20個職缺
    job_analysis = []
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)

    async with aiohttp.ClientSession() as session:
        tasks = [
            analyze_single_job(session, job, semaphore)
            for job in jobs
        ]
        
        print(f"\nStarting analysis of {len(jobs)} jobs...")
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # 過濾出成功的結果
        job_analysis = [
            result for result in results 
            if isinstance(result, tuple)
        ]

    print(f"Total {len(job_analysis)} job analyses completed")
    return job_analysis
