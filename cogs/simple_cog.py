import discord
from discord.ext import commands
from discord import app_commands
    
class SimpleCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @app_commands.command(name="kick", description="Kicks a member")
    async def kick(self, interaction: discord.Interaction, member: discord.Member, reason: str = None):
        await member.kick(reason=reason)
        await interaction.response.send_message(f"I kicked {member.mention}.", ephemeral=True)
    
async def setup(bot: commands.Bot):
    await bot.add_cog(SimpleCog(bot))