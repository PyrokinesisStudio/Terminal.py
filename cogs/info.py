import time
import discord
import psutil
import os

from discord.ext import commands
from assets import repo

mapsbaseurl = "https://maps.googleapis.com/maps/api/{ep}/json?{path}{dest}"


class Information:
    def __init__(self, bot):
        self.bot = bot
        self.process = psutil.Process(os.getpid())

    @commands.command()
    async def ping(self, ctx):
        """ Pong! """
        mesg = "pong"
        before = time.monotonic()
        pong = await ctx.send(mesg)
        after = time.monotonic()
        ping = (after - before) * 1000
        await pong.edit(content=f"{mesg}   |   {int(ping)}ms")

    @commands.command()
    async def source(self, ctx):
        """ Invite me to your server """
        await ctx.send(f"**{ctx.bot.user}** is powered by this source code:\nhttps://github.com/AlexFlipnote/discord_bot.py")

    @commands.command(aliases=['info', 'stats'])
    async def about(self, ctx):
        """ About the bot """
        ramUsage = self.process.memory_full_info().rss / 1024**2

        embed = discord.Embed(colour=0xC29FAF)
        embed.set_thumbnail(url=ctx.bot.user.avatar_url)
        embed.add_field(name="Developer", value="AlexFlipnote", inline=True)
        embed.add_field(name="Library", value="discord.py", inline=True)
        embed.add_field(name="Servers", value=len(ctx.bot.guilds), inline=True)
        embed.add_field(name="RAM", value=f"{ramUsage:.2f} MB", inline=True)

        await ctx.send(content=f"ℹ About **{ctx.bot.user}** | **{repo.version}**", embed=embed)


def setup(bot):
    bot.add_cog(Information(bot))
