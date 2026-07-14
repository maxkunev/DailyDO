from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from django.utils import timezone

# Django

import django
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
sys.path.append(PROJECT_ROOT)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dailydo.settings')
django.setup()

# Scheduler

import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from .jobs import proccess_tasks_morning, proccess_tasks_evening

async def main():
    
    scheduler = AsyncIOScheduler()

    scheduler.add_job(
        proccess_tasks_morning, 
        'cron', 
        hour=7,
        minute=0,
        timezone=ZoneInfo(os.getenv("TIMEZONE"))
    )

    scheduler.add_job(
        proccess_tasks_evening, 
        'cron', 
        hour=20,
        minute=00,
        timezone=ZoneInfo(os.getenv("TIMEZONE"))
    )

    scheduler.start()

    try:
        await asyncio.Event().wait()
    finally:
        scheduler.shutdown()
        
if __name__ == "__main__":
    asyncio.run(main())