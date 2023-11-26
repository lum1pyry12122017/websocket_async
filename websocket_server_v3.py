"""Websocket server, reads values from the csv file and stream values.

look files from folder: ./data_folder/ next to script.
Seclect file based on client request.

eg. request: 2,yyyy,0 meaninig int in filename, yyyy string in file name (not in use yet),
 int first column number. File name 2data.csv, line o will streamed.

Server will stream same line continously until server recive STOP or another request.


"""
import websockets
import asyncio
import csv
import numpy as np

class CsvWebSocketServer():
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.path = "./data_folder/"
        self.current_data = None
        self.current_request = None
        
    # read csv
    def read_csv(self, file_number: str, line_number: int):
        """Read csv file.
        """
        filename = self.path + f"data{file_number}.csv"
        # print(f"Open file: {filename}")

        try:
            with open(filename, newline="") as csv_file:
                reader = csv.reader(csv_file)
                result = []
                for i, row in enumerate(reader):
                    # print(f"Row nr {i}: {row}")
                    if row and int(row[0]) == line_number:
                        result.append(row)
                return result[0]
        except FileNotFoundError:
            print("File not found (read_csv method)")
            return None
        except ValueError:
            print("ValueError (read_csv method)")
            return None

    # websoket server, request from client to this server
    async def send_data_periodically(self, websocket):
        """Send message to client"""
        while True:
            if self.current_data:
                await websocket.send(str(self.current_data))
            await asyncio.sleep(np.random.randint(1,11))  # random delay between send

    async def ws_handler(self, websocket, path):
        """ws handler interpret requests"""
        send_data_task = None
        async for message in websocket:
            
            # handle received message
            try:
                print(f"Received message: {message}")
                if message.startswith("GET"):
                    _,file_number,file_name,line_number = message.split(",")
                    file_number = int(file_number)
                    line_number = int(line_number)
                    data = self.read_csv(file_number, line_number)
                    if data:
                        await websocket.send(str(data))
                    else:
                        await websoket.send("File not found (GET request)")

                elif message == "STOP":
                    if send_data_task:
                        send_data_task.cancel()
                        send_data_task = None
                    await websocket.send("Data sending stopped")
                elif message == "*IDN?":
                    await websocket.send(f"Server name CsvWebSocketServer, address: {self.host}, port: {self.port}")
                
                # csv line requests handled here
                else:
                    file_number, file_name, line_number = message.split(",")
                    file_number = int(file_number)
                    line_number = int(line_number)
                    file_name = str(file_name) # NOT uset yet

                    # store latest request (to recognice new requests)
                    self.current_request = (file_number, line_number)
                    
                    # validate request
                    if 0 <= file_number <= 5 and 0 <= line_number <= 360:
                        
                        #if requ ok read file
                        data = self.read_csv(file_number, line_number)
                        if data:
                            self.current_data = data
                            print("Data from file: ", data)
                        else:
                            await websocket.send("File not found (ws_handler)")
                    
                    # handle repeater (new requ or stop)
                    if not send_data_task or send_data_task.done():
                        send_data_task = asyncio.create_task(self.send_data_periodically(websocket))
                    else:
                        await websocket.send("UNEXCPECTED happend? (ws_handler)")
            except ValueError as e:
                print(f"Error parsing message: {e}")
                await websocket.send("Invalid request from client (value error ws_handler)")
    # start server
    async def start_server(self):
        async with websockets.serve(self.ws_handler, self.host,self.port):
            await asyncio.Future() 
    # create instance and call start server
server = CsvWebSocketServer("localhost", 8765)
asyncio.run(server.start_server())


