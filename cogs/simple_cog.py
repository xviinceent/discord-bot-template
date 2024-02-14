import discord
from discord.ext import commands
from discord import app_commands
    
class SimpleCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    # simple slash command for kicking a user with a provided reason. this command can be accessed using the slash command picker if you have proper permissions
    @app_commands.command(name="kick", description="Kicks a member")
    async def kick(self, interaction: discord.Interaction, member: discord.Member, reason: str = None):
        try:
            await member.kick(reason=reason)
            await interaction.response.send_message(f"I kicked {member.mention}.", ephemeral=True)
        except Exception as e:
            # if the bot is not allowed to kick the user, the bot will respond with this message
            if isinstance(e, discord.Forbidden):
                await interaction.response.send_message("I am not allowed to do that :(", ephemeral=True)
    
async def setup(bot: commands.Bot):
    await bot.add_cog(SimpleCog(bot))