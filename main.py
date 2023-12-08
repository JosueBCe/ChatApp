import json
import os
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
import httpx

load_dotenv()
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []
        self.messages: list[str] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

    """ CRUD messages operations """
    async def create_message(self, message: str):
        self.messages.append(message)
        await self.broadcast(message)

    def read_messages(self):
        return self.messages

    async def update_message(self, index: int, message: str, user_name:str):
        if index < len(self.messages):
            self.messages[index] = message  
            updated_message = f"Updated message:{index}:{message}:{user_name}"
            await self.broadcast(updated_message)

    async def delete_message(self, index: int):
        if index < len(self.messages):
            deleted_message = self.messages.pop(index)
            await self.broadcast(f"Message deleted:{index}")

manager = ConnectionManager()

""" HOME PAGE ENDPOINT """
@app.get("/")
async def get():
    return FileResponse("./templates/index.html")


@app.get("/github-login")
async def github_login():
    return RedirectResponse(f"https://github.com/login/oauth/authorize?client_id={os.getenv('GITHUB_CLIENT_ID')}", status_code=302)


templates = Jinja2Templates(directory="templates")


@app.get("/chatpage", response_class=HTMLResponse)
async def github_code(code: str, request: Request):
    params = {
        "client_id": os.getenv("GITHUB_CLIENT_ID"),
        "client_secret": os.getenv("GITHUB_CLIENT_SECRET"),
        "code": code,
    }
    headers = {"Accept": "application/json"}

    async with httpx.AsyncClient() as client:
        response = await client.post(url="https://github.com/login/oauth/access_token", params=params, headers=headers)
        response_json = response.json()
        access_token = response_json["access_token"]

    async with httpx.AsyncClient() as client:
        headers.update({"Authorization": f"Bearer {access_token}"})
        response = await client.get("https://api.github.com/user", headers=headers)
        user_info = response.json()

    # Store access_token in a variable
    access_token_value = access_token

    return templates.TemplateResponse(
        "chatpage.html",
        {"request": request, "user_info": user_info, "access_token": access_token_value},
        headers={"Content-Type": "text/html"},
    )

""" WEB SOCKET ENDPOINT """
@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            if data.startswith("create:"):
                message = data[len("create:"):]
                await manager.create_message(message)
            elif data.startswith("read"):
                messages = manager.read_messages()
                await manager.send_personal_message(str(messages), websocket)
            elif data.startswith("update:"):
                parts = data[len("update:"):].split(":")
                print(f"parts {parts}")
                if len(parts) == 4:
                    index = int(parts[0])
                    message = parts[2]
                    user_name = parts[3]
                    await manager.update_message(index, message, user_name)
            elif data.startswith("delete:"):
                index = int(data[len("delete:"):])
                await manager.delete_message(index)
            else:
                await manager.broadcast(f"{data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} has left the chat")

