import asyncio
import websockets
import csv
import json
from websocket_client_setings import *

class WebSocketClient:
    def __init__(self):
        self.connection = None

    async def connect(self):
        self.connection = await websockets.connect(SERVER_URL)
        # send requ to server
        await self.send_message("2,yyy,1")
        # await asyncio.sleep(13)
        # await self.send_message("STOP")
        # print("STOP sent")
        # await asyncio.sleep(1)
        # await self.send_message("GET,2,yyyy,1")
        # await asyncio.sleep(15)
        # await self.send_message("GET,2,yyyy,0")
        # await asyncio.sleep(15)
        # await self.send_message("GET,2,yyyy,3")
        # await asyncio.sleep(15)
        # print("Close connection")
        # await self.close()

    async def send_message(self, message):
        await self.connection.send(message)

    async def receive_message(self):
        async for message in self.connection:
            print("Received:", message)
            self.save_message(message)
            # Lisää toiminnallisuutta tähän tarvittaessa

    def save_message(self, message):
        try:
            message_list = json.loads(message)
        except json.JSONDecodeError:
            message_list = message.strip("[]").replace("'", "").split(", ")

        # Tallenna muunnetut arvot CSV-tiedostoon
        with open('messages.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(message_list)

    async def close(self):
        await self.connection.close()

    def run_forever(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.connect())
        loop.run_until_complete(self.receive_message())

if __name__ == "__main__":
    client = WebSocketClient()
    client.run_forever()
