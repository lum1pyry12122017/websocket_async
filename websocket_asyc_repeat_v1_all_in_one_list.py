import websockets
import asyncio
import csv

class CsvWebSocketServer():
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.path = "./data_folder/"
        self.current_data = None
        self.current_request = None
        
    # read csv
    def read_csv(self, file_number: str, line_number: int):
        filename = self.path + f"data{file_number}.csv"
        # print(f"Avataan tiedosto: {filename}")

        try:
            with open(filename, newline="") as csv_file:
                reader = csv.reader(csv_file)
                result = []
                for i, row in enumerate(reader):
                    # print(f"Rivi {i}: {row}")  # Tulostaa rivinumeron ja rivin
                    if row and int(row[0]) == line_number:
                        result.append(row)
                return result
        except FileNotFoundError:
            print("Tiedostoa ei löydy.")
            return None
        except ValueError:
            print("Virhe muunneltaessa rivin ensimmäistä saraketta kokonaisluvuksi.")
            return None

    # websoket server, request from client to this server
    async def send_data_periodically(self, websocket):
        while True:
            if self.current_data:
                await websocket.send(str(self.current_data))
            await asyncio.sleep(1)  # Lähettää dataa joka sekunti

    async def ws_handler(self, websocket, path):
        asyncio.create_task(self.send_data_periodically(websocket))
        async for message in websocket:
            try:
                file_number, file_name, line_number = message.split(",")
                file_number = int(file_number)
                line_number = int(line_number)

                # Säilytetään viimeisin pyyntö
                self.current_request = (file_number, line_number)

                if 0 <= file_number <= 5 and 0 <= line_number <= 360:
                    data = self.read_csv(file_number, line_number)
                    if data:
                        self.current_data = data
                        print("Data from file: ", data)
                    else:
                        await websocket.send("File not found")
                else:
                    await websocket.send("Invalid request")
            except ValueError:
                await websocket.send("Invalid message")
    # palvelimen käynnistys
    async def start_server(self):
        async with websockets.serve(self.ws_handler, self.host,self.port):
            await asyncio.Future() 
    # Luodaan ja käynnistetään palvelin
server = CsvWebSocketServer("localhost", 8765)
asyncio.run(server.start_server())


