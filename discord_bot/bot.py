import os
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
MIDJOURNEY_CHANNEL_ID = int(os.getenv("MIDJOURNEY_CHANNEL_ID"))

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ثبت کامند اسلش برای همه گیلدها (سرورها)
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands.")
    except Exception as e:
        print(f"Error syncing commands: {e}")

# دستور /prompt
@bot.tree.command(name="prompt", description="Send a prompt to Midjourney channel")
@app_commands.describe(text="The prompt text to send")
async def prompt(interaction: discord.Interaction, text: str):
    channel = bot.get_channel(MIDJOURNEY_CHANNEL_ID)
    if not channel:
        await interaction.response.send_message("❌ کانال Midjourney پیدا نشد.", ephemeral=True)
        return
    try:
        await channel.send(f"/imagine prompt: {text}")
        await interaction.response.send_message("✅ پرامپت با موفقیت ارسال شد.", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"❌ خطا در ارسال پرامپت: {e}", ephemeral=True)

bot.run(TOKEN)
