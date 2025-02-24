import asyncio
from aiohttp import web

from database import init_db
from job104 import scrape_and_save
from analyze import analyze_jobs_with_ai

async def health_check(request):
    return web.Response(text="OK", status=200)

async def start_server():
    app = web.Application()
    app.router.add_get('/health', health_check)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 8080)
    await site.start()

async def main():
    try:
        init_db()
        await asyncio.gather(
            start_server(),
            scrape_and_save()
        )
    except Exception as e:
        print(f"Error: {e}")
        return

if __name__ == "__main__":
    asyncio.run(main())            