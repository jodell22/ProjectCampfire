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

# Run the bot
bot.run(TOKEN)
