import discord
from discord.ext import commands
from discord import app_commands
# since we're working with an SQLite database, we have to import the aiosqlite library
import aiosqlite
from io import BytesIO
 
class DatabaseIntegrationExample(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # hybrid command for saving a file (can be executed via the slash command picker or by typing !save-file)
    @commands.hybrid_command(name="save-file")
    async def save_file(self, ctx: commands.Context, attachment: discord.Attachment | None):
        await ctx.defer(ephemeral=True)
        if attachment is None:
            await ctx.reply("You haven't selected a file!", ephemeral=True)
        else:
            if attachment.size / 1024 > 10000:
                await ctx.reply("File is too large! Maximum size is 10MB", ephemeral=True)
                return
            # connect to the database
            conn = await aiosqlite.connect("database.db")
            cursor = await conn.cursor()

            # convert the attachment to bytes
            attachment_bytes = await attachment.read()

            # insert the attachment into the database
            try:
                await cursor.execute("INSERT INTO files (SERVERID, FILEBYTES, FILENAME) VALUES (?, ?, ?)", (ctx.guild.id, attachment_bytes, attachment.filename,))
            except:
                await cursor.execute("UPDATE files SET FILEBYTES = ?, FILENAME = ? WHERE SERVERID = ?", (attachment_bytes, attachment.filename, ctx.guild.id,))

            await conn.commit()
            await cursor.close()
            await conn.close()
            await ctx.reply("File saved!", ephemeral=True)

    # hybrid command for loading the save file (can be executed via the slash command picker or by typing !load-file)
    @commands.hybrid_command(name="load-file")
    async def load_file(self, ctx: commands.Context):
        await ctx.defer()
        # connect to the database
        conn = await aiosqlite.connect("database.db")
        cursor = await conn.cursor()

        # select the attachment from the database
        await cursor.execute("SELECT FILEBYTES, FILENAME FROM files WHERE SERVERID = ?", (ctx.guild.id,))
        result = await cursor.fetchone()

        if result is None:
            await cursor.close()
            await conn.close()
            await ctx.reply("No file found!")
        else:
            # convert the attachment to bytes
            attachment_bytes = result[0]
            filename = result[1]
            file = BytesIO(attachment_bytes)

            # close the database
            await cursor.close()
            await conn.close()

            # send the attachment with correct file extension

            await ctx.reply(file=discord.File(file, filename=filename))
        
 
async def setup(bot: commands.Bot):
    await bot.add_cog(DatabaseIntegrationExample(bot))