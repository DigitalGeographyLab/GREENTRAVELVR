"""
Biopac WebSocket Bridge
Description:
## Biopac NDT API binding; 
  Receives messages from a WebSocket server and forwards events/markers to Biopac via biopacndt.
Usage:
  python ServerToBiopac.py

Notes:
  - Edit host/port or device IDs as needed.
"""
import os
import asyncio
import websockets
import biopacndt
import json
from termcolor import colored

# Biopac Acknowledge connection details
ACK_HOST = 'localhost'
ACK_PORT = 15010

GRT_PORT = 8080

title = "GTVL BIOPAC CMD"

async def send_data_via_websocket(websocket, data):
    """Send data to the WebSocket server."""
    try:
        await websocket.send(data)
    except Exception as e:
        print(f"Error sending data via WebSocket: {e}")

# Helper function to insert global events into Biopac
def insert_global_event(acqServer, event_type, event_id, description):
    try:
        retVal = acqServer.insertGlobalEvent(event_type, event_id, description)
        if retVal == 0:
            print(colored(f"Global event '{event_type}' with ID '{event_id}' inserted", 'yellow'))
        else :
            print(colored(f'Global Event Insertion Failed', 'red'))

    except Exception as e:
        print(f"Failed to insert global event: {e}")

# Function to handle messages received from the WebSocket server
async def handle_message(acqServer, websocket, message):
    print(f"Received message: {message}")
    # Handle messages received from the WebSocket server.
    try:
        data = json.loads(message)
        # Check if 'action' field exists and its value is 'statuscheck'
        if 'action' in data and data['action'] == 'statuscheck'and 'type' in data and data['type'] == 'dashboard':
            print("Received statuscheck ping. Sending response and checking cadence sensor...")
            statusString = "statuscheck"
            if acqServer.getAcquisitionInProgress():
                statusString = f"statuscheck-data-aquisition"
            data = { 
                    "type" : "biopac",
                    "action" : statusString
                    }
            data_str = json.dumps(data)

            # Forward this data to dashboard
            await send_data_via_websocket(websocket, data_str)
        if 'action' in data and data['action'] == 'checkpoint'and 'type' in data and data['type'] == 'ue5':
            print("Received checkpoint info")
            returnString = "checkpoint-insertion-failed-data-acq-not-running"
            if acqServer.getAcquisitionInProgress():
                returnString = f"checkpoint-inserted"
                insert_global_event(acqServer, data['message'], '1', '')
            data = { 
                    "type" : "biopac",
                    "action" : returnString
                    }
            data_str = json.dumps(data)

            # Forward this data to dashboard
            await send_data_via_websocket(websocket, data_str)
        else:
            print("Action field is missing or its value is not 'statuscheck'.")
    except json.JSONDecodeError:
        print("Data is not in JSON format.")

# Function to connect to Biopac
def connect_to_biopac():
    try:
        acqServer = biopacndt.AcqNdtQuickConnect()
        if not acqServer:
            print("No AcqKnowledge Server Found!")
            return None
        print(colored('Biopac connection successful', 'green'))
        return acqServer
    except biopacndt.BiopacNdtError as e:
        print(f"BiopacNdtError: {e}")
        return None

# Main function to connect to the WebSocket server and listen for messages
async def websocket_client():
    acqServer = connect_to_biopac()
    if not acqServer:
        return

    uri = f"ws://localhost:{GRT_PORT}"
    try:
        async with websockets.connect(uri) as websocket:
            print(colored(f'Connected to WebSocket server at {uri}', 'green'))
            while True:
                message = await websocket.recv()
                await handle_message(acqServer, websocket, message)
    except Exception as e:
        print(f"An error occurred with the WebSocket connection: {e}")

if __name__ == "__main__":
    # set window name first
    os.system(f'title {title}')
    asyncio.get_event_loop().run_until_complete(websocket_client())
