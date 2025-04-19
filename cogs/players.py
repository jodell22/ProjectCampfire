import discord
from discord.ext import commands
from db import helpers

USAGE_MSG = ("Usage:\n"
              "`!player set <name> key: value`\n"
              "`!player stats <name>`\n"
              "`!player list`\n"
              "`!player delete <name>`\n"
              "`!player clear`\n"
              "`!player claim <name>`\n"
              "`!player owner <name>`")

class Players(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def player(self, ctx, action=None, name=None, *, entry=None):
        if not action:
            await ctx.send(USAGE_MSG)
            return

        if action == "set" and name and entry:
            if not helpers.get_player_by_name(name):
                helpers.create_player(name, ctx.author.id)
            if ":" not in entry:
                await ctx.send("❌ Format: `!player set <name> key: value`")
                return
            key, value = map(str.strip, entry.split(":", 1))
            helpers.set_player_stat(name, key, value)
            await ctx.send(f"✅ Set **{key}** = {value} for **{name}**")

        elif action == "stats" and name:
            stats = helpers.get_player_stats(name)
            if stats is not None:
                stat_lines = [f"{k}: {v}" for k, v in stats.items()]
                await ctx.send(f"📜 Stats for **{name}**:\n" + "\n".join(stat_lines))
            else:
                await ctx.send(f"❌ No stats found for **{name}**")

        elif action == "list":
            players = helpers.get_all_players()
            if players:
                await ctx.send("📇 Known players:\n" + "\n".join(f"- {p}" for p in players))
            else:
                await ctx.send("📭 No players saved yet.")

        elif action == "delete" and name:
            if helpers.get_player_by_name(name):
                helpers.delete_player_by_name(name)
                await ctx.send(f"🗑️ Deleted player **{name}**")
            else:
                await ctx.send(f"❌ No player named **{name}**")

        elif action == "clear":
            players = helpers.get_all_players()
            if players:
                for p in players:
                    helpers.delete_player_by_name(p)
                await ctx.send("💥 All player data cleared.")
            else:
                await ctx.send("📭 No players to clear.")

        elif action == "claim" and name:
            if helpers.get_player_by_name(name):
                helpers.set_player_owner(name, ctx.author.id)
                await ctx.send(f"🪪 {name} is now claimed by {ctx.author.mention}")
            else:
                await ctx.send(f"❌ No player named **{name}**")

        elif action == "owner":
            if name:
                player = helpers.get_player_by_name(name)
                if player and player[2]:  # owner_id is at index 2
                    owner = await self.bot.fetch_user(player[2])
                    await ctx.send(f"👤 Owner of **{name}**: {owner.mention}")
                else:
                    await ctx.send(f"🤷‍♂️ No one has claimed **{name}** yet.")
            else:
                # Find player claimed by this user
                all_players = helpers.get_all_players()
                for pname in all_players:
                    player = helpers.get_player_by_name(pname)
                    if player and player[2] == ctx.author.id:
                        await ctx.send(f"🪪 You own **{pname}**")
                        return
                await ctx.send("🤷‍♂️ You haven't claimed any characters yet.")

        else:
            await ctx.send(USAGE_MSG)

async def setup(bot):
    await bot.add_cog(Players(bot))
