from assets import permissions
from concurrent.futures import ThreadPoolExecutor

try:
    import ujson as json
except ImportError:
    import json
from discord.ext.commands import AutoShardedBot as _Bot


class Bot(_Bot):
    def __init__(self, *args, prefix=None, **kwargs):
        with open("config.json") as f:
            self.config = json.load(f)
        self.prefix = prefix
        self.executor = ThreadPoolExecutor(max_workers=16)
        super().__init__(*args, **kwargs)

    async def on_message(self, msg):
        if not self.is_ready() or msg.author.bot or not permissions.can_send(msg):
            return

        await self.process_commands(msg)
