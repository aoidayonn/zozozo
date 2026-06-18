import json
from channels.generic.websocket import AsyncWebsocketConsumer

# ルーム管理（インメモリ）
rooms = {}  # { "room_name": [channel_name_1, channel_name_2] }


class TetrisConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"tetris_{self.room_name}"

        # ルームに参加
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        # ルームの参加者リストを更新
        if self.room_name not in rooms:
            rooms[self.room_name] = []
        rooms[self.room_name].append(self.channel_name)

        # プレイヤー番号を割り当て
        player_number = len(rooms[self.room_name])

        # 参加通知
        await self.send(text_data=json.dumps({
            "type": "joined",
            "player": player_number,
            "total": len(rooms[self.room_name]),
        }))

        # 2人揃ったらゲーム開始通知
        if len(rooms[self.room_name]) == 2:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "game_start",
                    "message": "対戦開始！",
                }
            )

    async def disconnect(self, close_code):
        # ルームから退出
        if self.room_name in rooms:
            if self.channel_name in rooms[self.room_name]:
                rooms[self.room_name].remove(self.channel_name)
            if not rooms[self.room_name]:
                del rooms[self.room_name]

        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

        # 相手に通知
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "opponent_left",
            }
        )

    async def receive(self, text_data):
        data = json.loads(text_data)

        # 相手にデータ転送（盤面状態・攻撃など）
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "relay",
                "sender": self.channel_name,
                "data": data,
            }
        )

    # ── ルーム全員に送るハンドラ ──
    async def relay(self, event):
        # 送信者以外に転送
        if event["sender"] != self.channel_name:
            await self.send(text_data=json.dumps(event["data"]))

    async def game_start(self, event):
        await self.send(text_data=json.dumps({
            "type": "game_start",
        }))

    async def opponent_left(self, event):
        await self.send(text_data=json.dumps({
            "type": "opponent_left",
        }))