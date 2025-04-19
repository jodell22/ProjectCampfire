# cogs/core.py
import discord
from discord.ext import commands
import openai
import os

class Core(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        openai.api_key = os.getenv("OPENAI_API_KEY")

    @commands.command()
    async def ping(self, ctx):
        await ctx.send("🏓 Pong!")

    @commands.command()
    async def asknova(self, ctx, *, question):
        await ctx.send("Thinking... 🔮")
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": question}],
                temperature=0.7
            )
            answer = response.choices[0].message.content.strip()
            await ctx.send(answer)
        except Exception as e:
            await ctx.send(f"Error: {e}")

async def setup(bot):
    await bot.add_cog(Core(bot))
