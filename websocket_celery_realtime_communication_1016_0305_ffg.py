# 代码生成时间: 2025-10-16 03:05:22
import os
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from celery import Celery
from asgiref.sync import sync_to_async
from myapp.tasks import send_message

# 设置Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
app = Celery('myapp')
app.config_from_object('django.conf:settings', namespace='CELERY')

# WebSocket消费者
class RealTimeConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # 用户连接时执行的操作
        self.room_group_name = 'chat_%s' % self.scope['url_route']['kwargs']['room_name']
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # 用户断开连接时执行的操作
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # 接收消息
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        # 使用Celery发送消息
        await sync_to_async(send_message.delay)(self.room_group_name, message)

    # 接收Celery发送的消息
    async def send_message_to_group(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({'message': message}))

# Celery任务
@app.task
def send_message(room_group_name, message):
    # 发送消息到组
    async_to_sync(RealTimeConsumer.send_message_to_group)(
        {},
        {'message': message}
    )

# 错误处理和日志记录可以添加到这里，例如：
# try:
#     # 尝试执行操作
# except Exception as e:
#     # 处理异常
#     # 记录日志
