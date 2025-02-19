import requests
import json
import time
import os

from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

def analyze_jobs_with_ai(jobs):
    if not OPENAI_API_KEY:
        print("OpenAI API Key not set, skip AI analysis")
        return []

    job_analysis = []
    for job in jobs[:20]:
        job_desc = job['description'] if 'description' in job else 'Not provided'
        job_no = job['jobNo'] if 'jobNo' in job else 'unknown'
        print(f"\nAnalyzing job {len(job_analysis) + 1}/20: {job_no}")
        
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

            response = requests.post("https://api.openai.com/v1/chat/completions", json=payload, headers=headers)
            print("\nOpenAI Response:")
            print(json.dumps(response.json(), indent=2, ensure_ascii=False)) 
            
            if response.status_code == 200:
                result = response.json()
                ai_content = result["choices"][0]["message"]["content"]
                print(f"AI response: {ai_content}")  

                try:
                    ai_response = json.loads(ai_content)
                    skills = json.dumps(ai_response['skills'], ensure_ascii=False)
                    job_analysis.append((job_no, skills))
                    time.sleep(3)
                except Exception as e:
                    print(f"Error parsing AI response: {str(e)}")
            else:
                print(f"AI analysis failed, status code: {response.status_code}")
                time.sleep(5)  
                
        except Exception as e:
            print(f"Error analyzing job: {str(e)}")
            time.sleep(5)
    
    print(f"Total {len(job_analysis)} job analyses completed")
    return job_analysis
