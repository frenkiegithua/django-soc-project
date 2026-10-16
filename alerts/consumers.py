import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Alert, Incident


class AlertConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("alerts", self.channel_name)
        await self.accept()
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("alerts", self.channel_name)
    
    async def alert_update(self, event):
        await self.send(text_data=json.dumps(event["data"]))


class DashboardConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("dashboard", self.channel_name)
        await self.accept()
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("dashboard", self.channel_name)
    
    async def dashboard_update(self, event):
        await self.send(text_data=json.dumps(event["data"]))
