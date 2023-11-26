import discord
from discord.ext import commands
from discord import app_commands
    
class SimpleCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    # simple slash command for kicking a user with a provided reason. this can be accessed via the slash command picker if you have proper permissions
    @app_commands.command(name="kick", description="Kicks a member")
    async def kick(self, interaction: discord.Interaction, member: discord.Member, reason: str = None):
        await member.kick(reason=reason)
        await interaction.response.send_message(f"I kicked {member.mention}.", ephemeral=True)
    
async def setup(bot: commands.Bot):
    await bot.add_cog(SimpleCog(bot))