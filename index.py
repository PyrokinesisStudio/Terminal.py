import json
import os

from assets import permissions
from data import Bot
from discord.ext.commands import HelpFormatter

class HelpFormat(HelpFormatter):
    async def format_help_for(self, context, command_or_bot):
        if permissions.can_react(context):
            await context.message.add_reaction(chr(0x2705))

        return await super().format_help_for(context, command_or_bot)


help_attrs = dict(hidden=True)

with open("config.json") as f:
    data = json.load(f)
    token = data["token"]
    prefix = data["prefix"]

description = """
Terminal.py, a bot that is made to be used in terminal server
"""

bot = Bot(command_prefix=prefix,
          prefix=prefix,
          description=description,
          pm_help=True,
          help_attrs=help_attrs,
          formatter=HelpFormat())

for file in os.listdir("cogs"):
        if file.endswith(".py"):
            name = file[:-3]
            bot.load_extension(f"cogs.{name}")

bot.run(token)
