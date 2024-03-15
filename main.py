import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import aiosqlite

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


load_dotenv()
bot.run(os.getenv("TOKEN"))
