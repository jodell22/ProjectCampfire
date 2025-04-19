import discord
from discord.ext import commands

class PlayerMenu(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="📋 View Stats", style=discord.ButtonStyle.primary, custom_id="view_stats")
    async def view_stats(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("🔍 Use `!player stats <name>` to view stats.", ephemeral=True)

    @discord.ui.button(label="📝 Set Stat", style=discord.ButtonStyle.primary, custom_id="set_stat")
    async def set_stat(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("✏️ Use `!player set <name> key: value` to set a stat.", ephemeral=True)

    @discord.ui.button(label="➕ Add Player", style=discord.ButtonStyle.success, custom_id="add_player")
    async def add_player(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("➕ Use `!player set <name> class: ...` to add a new player.", ephemeral=True)

    @discord.ui.button(label="🗑️ Delete Player", style=discord.ButtonStyle.danger, custom_id="delete_player")
    async def delete_player(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("🗑️ Use `!player delete <name>` to delete a player.", ephemeral=True)

class PlayerUI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def playermenu(self, ctx):
        view = PlayerMenu()
        await ctx.send("📂 Player Management Menu:", view=view)

async def setup(bot):
    await bot.add_cog(PlayerUI(bot))
