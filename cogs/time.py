import discord
from discord.ext import commands
from db.helpers import world_time
from datetime import datetime, timedelta
import re
import inspect

class Time(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def parse_time_delta(self, input_str):
        pattern = r"(\d+)([mhdMt])"
        matches = re.findall(pattern, input_str)
        if not matches:
            raise ValueError("No valid time intervals found. Use 1t, 15m, 2h, 1d, 1M.")

        delta = timedelta()
        turns = 0

        for value, unit in matches:
            value = int(value)
            if unit == "m":
                delta += timedelta(minutes=value)
            elif unit == "h":
                delta += timedelta(hours=value)
            elif unit == "d":
                delta += timedelta(days=value)
            elif unit == "M":
                delta += timedelta(days=30 * value)  # Approximate 1 month as 30 days
            elif unit == "t":
                turns += value

        return delta, turns

    @commands.command()

    async def time(self, ctx, action=None, *, arg=None):

        if not action or action == "now":
            date, time_str, turns, notes = world_time.get_world_time()
            await ctx.send(
                f"🕰️ Current world time (from DB):\n"
                f"Date: **{date}**\nTime: **{time_str}**\nTurns Passed: **{turns}**"
            )
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
                delta, turns = self.parse_time_delta(arg)
                date, time_str, old_turns, notes = world_time.get_world_time()

                dt = datetime.strptime(f"{date} {time_str}", "%Y-%m-%d %H:%M:%S")
                new_dt = dt + delta
                world_time.set_world_time(new_dt.strftime("%Y-%m-%d"), new_dt.strftime("%H:%M:%S"))

                if turns > 0:
                    world_time.increment_turns(turns)

                await ctx.send(f"⏩ Advanced time to **{new_dt.strftime('%Y-%m-%d')} {new_dt.strftime('%H:%M')}** and added **{turns}** turn(s)")
            except Exception as e:
                await ctx.send(f"❌ Error: {str(e)}. Use format like `!time advance 2h`, `!time advance 1t 15m`, etc.")
            return

        await ctx.send("❌ Usage:\n`!time now`\n`!time set <date>, <time>`\n`!time advance <value>` (e.g., `1t`, `2h`, `15m`, `1d`, `1M`)\nYou can combine values like `1t 3h 30m`.")

async def setup(bot):
    await bot.add_cog(Time(bot))
