import os
import discord
from discord.ext import commands
import openai
from dotenv import load_dotenv

# Load .env file
load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Setup OpenAI
openai.api_key = OPENAI_API_KEY

# Setup Bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Basic ping command
@bot.command()
async def ping(ctx):
    await ctx.send("🏓 Pong!")

# AskNova command using OpenAI
@bot.command()
async def asknova(ctx, *, question):
    await ctx.send("Thinking... 🔮")
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": question}],
            temperature=0.7
        )
        answer = response.choices[0].message.content.strip()
        await ctx.send(answer)
    except Exception as e:
        await ctx.send(f"Error: {e}")

# Start the bot
bot.run(TOKEN)
