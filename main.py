import os
import discord
from discord.ext import commands
import openai
from dotenv import load_dotenv

custom_system_prompts = {}

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

@bot.command()
async def narrate(ctx, *, text):
    if ctx.channel.id != DM_ROOM_ID:
        return

    world_channel = bot.get_channel(WORLD_ROOM_ID)
    if world_channel:
        await world_channel.send(f"*{text}*")

@bot.command()
async def narrategpt(ctx, *, instruction):
    if ctx.channel.id != DM_ROOM_ID:
        return

    system_prompt = (
        "You are Nova, the in-world narrator. "
        "Respond with vivid, third-person narration only. "
        "Never break character or address the players directly. "
        "Imagine you're writing a high-fantasy novel."
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": instruction}
    ]

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=messages,
            temperature=0.85
        )
        narration = response.choices[0].message.content.strip()
        world_channel = bot.get_channel(WORLD_ROOM_ID)
        if world_channel:
            await world_channel.send(f"*{narration}*")
    except Exception as e:
        await ctx.send(f"Error: {e}")

@bot.command()
async def nova_prompt(ctx, *, system_prompt):
    if ctx.channel.id != DM_ROOM_ID:
        return

    custom_system_prompts[ctx.guild.id] = system_prompt
    await ctx.send(f"🧠 System prompt updated!")

# Basic ping command
@bot.command()
async def ping(ctx):
    await ctx.send("🏓 Pong!")

# AskNova command using OpenAI
@bot.command()
async def asknova(ctx, *, question):
    if ctx.channel.id not in [DM_ROOM_ID, WORLD_ROOM_ID]:
        return

    # Get custom prompt or fallback
    system_prompt = custom_system_prompts.get(ctx.guild.id, "You are Nova, the helpful in-world narrator.")

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": question}
    ]

    await ctx.send("Thinking... 🔮")

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=messages,
            temperature=0.7
        )
        answer = response.choices[0].message.content.strip()
        await ctx.send(answer)

    except Exception as e:
        await ctx.send(f"Error: {e}")



# Start the bot
bot.run(TOKEN)
