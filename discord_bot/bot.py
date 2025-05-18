import os
import discord
from dotenv import load_dotenv

load_dotenv()  # بارگذاری متغیرهای محیطی از فایل .env

TOKEN = os.getenv("DISCORD_BOT_TOKEN")

intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        await message.channel.send('Hello! I am your Cortex bot.')

client.run(TOKEN)
