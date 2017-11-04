import discord
import traceback

from assets import repo
from discord.ext.commands import errors


async def send_cmd_help(ctx):
    if ctx.invoked_subcommand:
        _help = await ctx.bot.formatter.format_help_for(ctx, ctx.invoked_subcommand)
    else:
        _help = await ctx.bot.formatter.format_help_for(ctx, ctx.command)

    for page in _help:
        await ctx.send(page)


def join_message(name, bot=True):
    return f"```ini\n[ New account has joined ]\nname = {name}\nbot = {bot}```"


class Events:
    def __init__(self, bot):
        self.bot = bot

    async def on_member_join(self, user):
        if user.bot is True:
            therole = discord.Object(id=352463488146341888)
            await self.bot.get_channel(repo.default_channel).send(join_message(user, bot=True))
            await user.add_roles(therole, reason="User joined | Bot account")
        else:
            therole = discord.Object(id=352460381119053825)
            await self.bot.get_channel(repo.default_channel).send(join_message(user, bot=False))
            await user.add_roles(therole, reason="User joined | User account")

    async def on_ready(self):
        print(f'{self.bot.user} is now ready!')
        await self.bot.change_presence(game=discord.Game(type=0, name="with beers 🍻"), status=discord.Status.dnd)

    async def on_command_error(self, ctx, err):
        if isinstance(err, errors.MissingRequiredArgument) or isinstance(err, errors.BadArgument):
            await send_cmd_help(ctx)

        elif isinstance(err, errors.CommandInvokeError):
            err = err.original

            _traceback = traceback.format_tb(err.__traceback__)
            _traceback = ''.join(_traceback)
            error = ('```py\n{2}{0}: {3}\n```').format(type(err).__name__, ctx.message.content, _traceback, err)

            await ctx.send(f"There was an error processing the command ;-;\n{error}")

        elif isinstance(err, errors.CheckFailure):
            pass

        elif isinstance(err, errors.CommandOnCooldown):
            await ctx.send(f"This command is on cooldown... try again in {err.retry_after:.0f} seconds.")

        elif isinstance(err, errors.CommandNotFound):
            pass


def setup(bot):
    bot.add_cog(Events(bot))
