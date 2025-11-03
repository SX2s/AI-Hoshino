import discord
from discord.ext import commands
import datetime
import os
import asyncio

# -------------------------------
# BOT SETTINGS
# -------------------------------

PREFIX = "!"
TOKEN = "your bot token"
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents, help_command=None)

# -------------------------------
# BOT EVENTS
# -------------------------------

@bot.event
async def on_ready():
    if bot.user is not None:
        print(f"✅ Logged in as: {bot.user.name} ({bot.user.id})")
    else:
        print("✅ Logged in, but bot.user is None")
    print(f"🌐 Connected to {len(bot.guilds)} servers")
    print(f"💬 Watching {sum((g.member_count or 0) for g in bot.guilds)} users")
    print("------------------------------")

# -------------------------------
# LOAD COGS AUTOMATICALLY
# -------------------------------

async def load_cogs(Cogs_folder="Cogs"):
    """Automatically load all .py cogs in the specified folder."""
    for filename in os.listdir(Cogs_folder):
        if filename.endswith(".py") and filename not in ("bot.py", "__init__.py"):
            try:
                await bot.load_extension(f"{Cogs_folder}.{filename[:-3]}")
                print(f"✅ Loaded cog: {filename}")
            except Exception as e:
                print(f"❌ Failed to load cog {filename}: {e}")

# -------------------------------
# MAIN STARTUP
# -------------------------------

async def main():
    async with bot:
        await load_cogs("Cogs")
        await bot.start(TOKEN)
        await bot.load_extension("ping")


# -------------------------------
# RUN THE BOT
# -------------------------------

asyncio.run(main())

