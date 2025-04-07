import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import aiosqlite
from discord import app_commands
import gtts
from io import BytesIO
import asyncio

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix = "!",
            intents = discord.Intents.all())

    async def setup_hook(self):
        # loads all extensions in the cogs folder
        for f in os.listdir("./cogs"):
            if f.endswith(".py"):
                await self.load_extension("cogs." + f[:-3])
        print("Loaded all extensions.")
        conn = await aiosqlite.connect("database.db")
        cursor = await conn.cursor()
        # creates the files table if it doesn't exist
        await cursor.execute("CREATE TABLE IF NOT EXISTS files (SERVERID INTEGER PRIMARY KEY, FILEBYTES TEXT, FILENAME TEXT)")
        await conn.commit()
        await cursor.close()
        await conn.close()
        await bot.tree.sync()

    async def on_ready(self):
        print(f'{self.user} is now online. [{self.user.id}]')

            
bot = MyBot()

# example message command: can be accessed by typing !ping in the chat
@bot.command()
async def ping(ctx: commands.Context):
    await ctx.send(f'🏓 Pong! Latency: {round(bot.latency * 1000)}ms')

@bot.tree.command(name="tts")
@app_commands.checks.cooldown(1, 15, key=lambda i: i.guild_id)
async def tts_command(interaction: discord.Interaction, text: app_commands.Range[str, 1, 100]):
    await interaction.response.defer(ephemeral=True)
    if interaction.user.voice:
        tts = gtts.gTTS(text, lang="en")
        audio_bytes = BytesIO()
        tts.write_to_fp(audio_bytes)
        audio_bytes.seek(0)

        voice_channel = interaction.user.voice.channel
        if interaction.guild.voice_client is not None:
            await interaction.guild.voice_client.move_to(voice_channel)
        else:
            await voice_channel.connect()

        voice_client = interaction.guild.voice_client
        audio_source = discord.FFmpegPCMAudio(audio_bytes, pipe=True)
        voice_client.play(audio_source)

        while voice_client.is_playing():
            await asyncio.sleep(1)

        await voice_client.disconnect()

        await interaction.followup.send("Done!", ephemeral=True)
    else:
        await interaction.followup.send("You need to be in a voice channel to use this command.", ephemeral=True)

@tts_command.error
async def tts_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.CommandOnCooldown):
        await interaction.response.send_message(f"This command is on cooldown and can be used in `{round(error.retry_after)}` seconds.", ephemeral=True)
    else:
        raise error

load_dotenv()
bot.run(os.getenv("TOKEN"))
