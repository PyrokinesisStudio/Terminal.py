from assets import repo
from discord.ext import commands


class Admin:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def amiadmin(self, ctx):
        """ Are you admin? """
        if ctx.author.id in repo.owners:
            return await ctx.send(f"Yes **{ctx.author.name}** you are admin! ✅")

        await ctx.send(f"no, heck off {ctx.author.name}")

    @commands.command()
    @commands.check(repo.is_owner)
    async def reload(self, ctx, name: str):
        """ Reloads an extension. """
        try:
            self.bot.unload_extension(f"cogs.{name}")
            self.bot.load_extension(f"cogs.{name}")
        except Exception as e:
            return await ctx.send(f"```\n{e}```")
        await ctx.send(f"Reloaded extension **{name}.py**")


def setup(bot):
    bot.add_cog(Admin(bot))
