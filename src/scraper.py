import asyncio

from database import init_db
from job104 import scrape_and_save
from analyze import analyze_jobs_with_ai

async def main():
    try: 
        init_db()
        await scrape_and_save()
    except KeyboardInterrupt:
        print("KeyboardInterrupt: Exiting gracefully...")
        return
    except Exception as e:
        print(f"Error initializing database: {e}")
        return    

if __name__ == "__main__":
    asyncio.run(main())            