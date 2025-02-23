from typing import Dict, Any

class BaseConfig:
    # Database
    DB_PATH: str = "data/jobs.db"
    
    # API Configuration
    API_CONFIG: Dict[str, Any] = {
        'URL': "https://www.104.com.tw/jobs/search/api/jobs",
        'HEADERS': {
            "User-Agent": "Mozilla/5.0",
            "Referer": "https://www.104.com.tw/jobs/search/?remoteWork=1",
            "Accept": "application/json"
        },
        'PARAMS': {
            "isJobList": 1,
            "jobcat": "2007001004,2007001016",
            "remoteWork": 1,
        }
    }
    
    # OpenAI Configuration
    MAX_CONCURRENT_REQUESTS: int = 3
    RATE_LIMIT_DELAY: int = 3