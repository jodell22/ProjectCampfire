# main.py
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Load .env file
load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

# Setup Bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Load extensions (cogs)
@bot.event
async def setup_hook():
    await bot.load_extension("cogs.core")
    await bot.load_extension("cogs.dice")
    await bot.load_extension("cogs.memory")
    await bot.load_extension("cogs.players")
    await bot.load_extension("cogs.playerui")
    await bot.load_extension("cogs.time")

    # Optional: Sync to a specific test guild for faster dev cycle
    GUILD_ID = 411698696514699286  # 🔁 Replace with your test server's ID
    guild = discord.Object(id=GUILD_ID)
    await bot.tree.sync(guild=guild)
    print(f"✅ Slash commands synced to guild {GUILD_ID}")

    print("📋 Commands currently registered in this guild:")
    for command in bot.tree.get_commands(guild=guild):
        print(f" - /{command.name}: {command.description}")

# Run the bot
bot.run(TOKEN)
