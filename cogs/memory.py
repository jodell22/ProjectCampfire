import discord
from discord.ext import commands
from db import helpers

MEMORY_USAGE_MSG = ("Usage:\n"
                    "`!remember key: value`\n"
                    "`!recall key`\n"
                    "`!memlist`\n"
                    "`!forget key`\n"
                    "`!memclear`")

class Memory(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def remember(self, ctx, *, entry=None):
        if not entry or ":" not in entry:
            await ctx.send(MEMORY_USAGE_MSG)
            return
        key, value = map(str.strip, entry.split(":", 1))
        helpers.set_memory(key, value)
        await ctx.send(f"🧠 Remembered: **{key}** → {value}")

    @commands.command()
    async def recall(self, ctx, *, key=None):
        if not key:
            await ctx.send(MEMORY_USAGE_MSG)
            return
        value = helpers.get_memory(key)
        if value:
            await ctx.send(f"📖 {key}: {value}")
        else:
            await ctx.send("🤔 I don't remember that one.")

    @commands.command()
    async def memlist(self, ctx):
        memory = helpers.get_all_memory()
        if not memory:
            await ctx.send("🧠 Memory is empty.")
            return
        keys = sorted(memory.keys())
        await ctx.send("🧾 Known entries:\n" + "\n".join(f"- {k}" for k in keys))

    @commands.command()
    async def forget(self, ctx, *, key=None):
        if not key:
            await ctx.send(MEMORY_USAGE_MSG)
            return
        if helpers.get_memory(key):
            helpers.delete_memory(key)
            await ctx.send(f"🗑️ Forgot: **{key}**")
        else:
            await ctx.send("🤔 I don't remember that one.")

    @commands.command()
    async def memclear(self, ctx):
        helpers.clear_memory()
        await ctx.send("💥 All memory cleared.")

async def setup(bot):
    await bot.add_cog(Memory(bot))
