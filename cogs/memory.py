import discord
from discord import app_commands
from discord.ext import commands
from memoryManager import addMemory

class MemoryCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("📌 MemoryCog initialized")

    @commands.hybrid_command(name="remember", description="Record a memory for a character or player")
    async def remember(
        self, ctx: commands.Context,
        subject: str,
        text: str,
        tags: str = ""
    ):
        try:
            tag_list = [tag.strip() for tag in tags.split(",")] if tags else []
            addMemory(subject=subject, text=text, tags=tag_list)
            await ctx.reply(
                f"💾 Memory saved for **{subject}**:\n> {text}", ephemeral=True
            )
        except Exception as e:
            await ctx.reply(
                f"⚠️ Error storing memory: {e}", ephemeral=True
            )

    @commands.hybrid_command(name="recall", description="View stored memories for a subject")
    async def recall(self, ctx: commands.Context, subject: str):
        from memoryManager import listMemories
        try:
            entries = listMemories(subject)
            if not entries:
                await ctx.reply(f"🔍 No memories found for **{subject}**.", ephemeral=True)
                return

            response = f"🧠 Memories for **{subject}**:\n"
            for mid, _, text in entries[:5]:
                response += f"- {text}\n"

            await ctx.reply(response, ephemeral=True)
        except Exception as e:
            await ctx.reply(f"⚠️ Error retrieving memories: {e}", ephemeral=True)



async def setup(bot):
    await bot.add_cog(MemoryCog(bot))

