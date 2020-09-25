#!/usr/bin/env python

import asyncio
import json
import websockets

async def send_command():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:

        msg = json.dumps({'cmd':'asfd'})
        await websocket.send(msg)
        response = await websocket.recv()
        print(response)

asyncio.get_event_loop().run_until_complete(send_command())