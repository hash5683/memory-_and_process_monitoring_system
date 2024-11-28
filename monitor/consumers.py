import psutil
from channels.generic.websocket import AsyncWebsocketConsumer
import json
import asyncio

class StatsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        while True:
            stats = {
                'cpu_percent': psutil.cpu_percent(interval=1),
                'memory_percent': psutil.virtual_memory().percent,
                'process_list': [
                    proc.info for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent'])
                ]
            }
            await self.send(text_data=json.dumps(stats))
            await asyncio.sleep(2)
