import discord
from discord.ext import commands
from db.helpers import world_time

class Time(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def time(self, ctx, action=None, *, arg=None):
        if not action or action == "now":
            date, time_str, turns, notes = world_time.get_world_time()
            await ctx.send(f"🕰️ Current world time:\nDate: **{date}**\nTime: **{time_str}**\nTurns Passed: **{turns}**")
            return

        if action == "set" and arg:
            if "," in arg:
                date_str, time_str = map(str.strip, arg.split(",", 1))
                world_time.set_world_time(date_str, time_str)
                await ctx.send(f"📅 Time updated to **{date_str}**, **{time_str}**")
            else:
                await ctx.send("❌ Use format: `!time set <date>, <time>`")
            return

        if action == "advance" and arg:
            try:
                count = int(arg.split()[0])
                world_time.increment_turns(count)
                await ctx.send(f"⏩ Advanced **{count}** turn(s)")
            except:
                await ctx.send("❌ Use format: `!time advance <#>` (e.g., `!time advance 1`)")
            return

        await ctx.send("❌ Usage:\n`!time now`\n`!time set <date>, <time>`\n`!time advance <#> turn[s]")

async def setup(bot):
    await bot.add_cog(Time(bot))
