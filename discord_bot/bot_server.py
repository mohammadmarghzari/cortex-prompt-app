import os
import discord
from discord.ext import commands
from fastapi import FastAPI, Request
import uvicorn
from dotenv import load_dotenv
import asyncio

load_dotenv()

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
MIDJOURNEY_CHANNEL_ID = int(os.getenv("MIDJOURNEY_CHANNEL_ID"))

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

app = FastAPI()

# وقتی ربات آماده شد
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")

# مسیر API برای دریافت پرامپت از استریم‌لیت
@app.post("/send_prompt/")
async def send_prompt(request: Request):
    data = await request.json()
    prompt_text = data.get("prompt", None)
    if not prompt_text:
        return {"status": "error", "message": "No prompt provided"}

    channel = bot.get_channel(MIDJOURNEY_CHANNEL_ID)
    if not channel:
        return {"status": "error", "message": "Midjourney channel not found"}

    # چون FastAPI تو یک ترد جدا اجرا میشه، برای ارسال پیام باید در حلقه اصلی async ربات اجرا کنیم
    await bot.loop.create_task(channel.send(f"/imagine prompt: {prompt_text}"))
    return {"status": "success", "message": "Prompt sent to Discord"}

def run_bot():
    # استارت همزمان FastAPI و ربات دیسکورد
    import threading

    def start_bot():
        bot.run(TOKEN)

    threading.Thread(target=start_bot).start()

    # استارت FastAPI
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    run_bot()
