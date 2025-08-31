from fastapi import WebSocket
from typing import Dict, List
import json

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, WebSocket] = {}
    
    async def connect(self, websocket: WebSocket, user_id: int):
        await websocket.accept()
        self.active_connections[user_id] = websocket
    
    def disconnect(self, user_id: int):
        if user_id in self.active_connections:
            del self.active_connections[user_id]
    
    async def send_personal_message(self, message: str, user_id: int):
        if user_id in self.active_connections:
            websocket = self.active_connections[user_id]
            try:
                await websocket.send_text(message)
            except Exception:
                self.disconnect(user_id)
    
    async def broadcast(self, message: str):
        disconnected_users = []
        
        for user_id, websocket in self.active_connections.items():
            try:
                await websocket.send_text(message)
            except Exception:
                disconnected_users.append(user_id)
        
        for user_id in disconnected_users:
            self.disconnect(user_id)
    
    async def send_to_role(self, message: str, target_role: str, exclude_user: int = None):
        await self.broadcast(message)
