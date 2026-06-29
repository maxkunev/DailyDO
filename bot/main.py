# Django

import django
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
sys.path.append(PROJECT_ROOT)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dailydo.settings')
django.setup()

# Aiogram

import asyncio
from aiogram import Bot, Dispatcher
from handlers import user



async def main():
    TOKEN_TG=os.getenv("TOKEN_TG")
    if not TOKEN_TG:
        raise ValueError("Token is not set")
    
    bot = Bot(token=TOKEN_TG)
    
    dp = Dispatcher()
    dp.include_router(user)
    
    await dp.start_polling(bot)
    
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped")