#!/usr/bin/env python

import asyncio
import datetime
import json
import websockets

def validate_message(msg):
    # super basic validation just checks that cmd exists
    return 'cmd' in msg

async def message_handler(websocket, path):

    while True:
        async for json_msg in websocket:
            
            msg = None
            response = {'cmd':'INVALID','status':'ERROR', 'message':'Unknown server error 🤷‍♂️'}
            
            try:
                msg = json.loads(json_msg)
                if not validate_message(msg):
                    response['message'] = 'Invalid message format'
                    await websocket.send(json.dumps(response))
                    continue
            except:
                response['message'] = 'Unable to decode JSON message'
                await websocket.send(json.dumps(response))
                continue


            # Message handlers
            def ping():
                return {'cmd':'ping', 'status':'OK', 'servertime':str(datetime.datetime.now())}

            def default():
                return {'cmd':msg['cmd'], 'status':'ERROR', 'message':'Unknown command:' + msg['cmd']}


            # I saw this interesting way to implement a switch statement:
            # https://www.simplifiedpython.net/python-switch-case-statement/
            dict = {
                'ping':ping
            }
            response = dict.get(msg['cmd'],default)()


            print('received ' + json_msg)
            await websocket.send(json.dumps(response))


start_server = websockets.serve(message_handler, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()