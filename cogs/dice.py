import discord
from discord.ext import commands
import random
import re

class Dice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def roll(self, ctx, *, expression: str):
        match = re.fullmatch(r'(\d*)d(\d+)([+-]\d+)?', expression.replace(" ", ""))
        if not match:
            await ctx.send("❌ Invalid format. Try `!roll d20`, `!roll 2d6+3`")
            return

        num_dice = int(match[1]) if match[1] else 1
        die_size = int(match[2])
        modifier = int(match[3]) if match[3] else 0

        if num_dice > 100:
            await ctx.send("❌ Too many dice! Max is 100.")
            return

        rolls = [random.randint(1, die_size) for _ in range(num_dice)]
        total = sum(rolls) + modifier

        mod_text = f" {match[3]}" if match[3] else ""
        await ctx.send(f"🎲 Rolls: {rolls}{mod_text} = **{total}**")

async def setup(bot):
    await bot.add_cog(Dice(bot))
