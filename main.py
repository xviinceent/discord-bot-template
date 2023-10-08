import discord
from discord.ext import commands
import os
import aiohttp
from dotenv import load_dotenv

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix = "!",
            intents = discord.Intents.all())

    async def setup_hook(self):
        self.session = aiohttp.ClientSession()
        for f in os.listdir("./cogs"):
            if f.endswith(".py"):
                await self.load_extension("cogs." + f[:-3])
        print("Loaded all extensions.")
        await bot.tree.sync()

    async def on_ready(self):
        print(f'{self.user} is now online. [{self.user.id}]')

            
bot = MyBot()

@bot.command()
async def ping(ctx: commands.Context):
    await ctx.send(f'🏓 Pong! {round(bot.latency * 1000)}ms')

load_dotenv()
bot.run(os.getenv("TOKEN"))
