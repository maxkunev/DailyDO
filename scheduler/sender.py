from aiogram import Bot
import os
import asyncio

bot = Bot(token=os.getenv("TOKEN_TG"))

async def send_task(chat_id, text):
    await bot.send_message(chat_id=chat_id, text=text)