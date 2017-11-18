from assets import permissions
from concurrent.futures import ThreadPoolExecutor

try:
    import ujson as json
except ImportError:
    import json
from discord.ext.commands import AutoShardedBot


class Bot(AutoShardedBot):
    def __init__(self, *args, **kwargs):
        with open("config.json") as f:
            self.config = json.load(f)
        self.prefix = kwargs.get("prefix")
        self.executor = ThreadPoolExecutor(max_workers=16)
        super().__init__(*args, **kwargs)

    async def on_message(self, msg):
        if self.is_ready() and not msg.author.bot and permissions.can_send(msg):
            await self.process_commands(msg)
