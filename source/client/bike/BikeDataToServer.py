"""
Cadence BLE → WebSocket Bridge
Description:
## BLE stack via bleak; ensure adapter permissions are set.
  Scans for BLE cycling cadence/crank sensors with bleak/pycycling and publishes readings over WebSockets.
Usage:
  python BikeDataToServer.py 
Notes:
  - Can read data from cadence or speed sensors.
  - Edit host/port as needed.
  - Get device IDs from the sensor and update the 'device_address', currently placeholder 'XX:XX:XX:XX:XX:XX'  
"""
import os
import asyncio
from bleak import BleakScanner, BleakClient
from pycycling.cycling_speed_cadence_service import CyclingSpeedCadenceService
import websockets
import json

# Replace this with your device's Bluetooth address
device_address = "XX:XX:XX:XX:XX:XX"

# WebSocket server details
WEBSOCKET_SERVER_URI = 'ws://localhost:8080'

# title of the window
title = "GTVL CADENCE BIKE CMD"

# Bleak client
client = None 

async def send_data_via_websocket(websocket, data):
    """Send data to the WebSocket server."""
    try:
        await websocket.send(data)
    except Exception as e:
        print(f"Error sending data via WebSocket: {e}")

async def handle_server_message(message, websocket):
    """Handle messages received from the WebSocket server."""
    global client  # Declare client as global to modify it within this function
    print("Received message from server:", message)
    try:
        data = json.loads(message)
        # Check if 'action' field exists and its value is 'statuscheck'
        if 'action' in data and data['action'] == 'statuscheck'and 'type' in data and data['type'] == 'dashboard':
            print("Received statuscheck ping. Sending response and checking cadence sensor...")
            data = { 
                    "type" : "bike",
                    "action" : "statuscheck"
                    }
            data_str = json.dumps(data)
            await send_data_via_websocket(websocket, data_str)
            # if not client.is_connected:
            #     print("Client is disconnected. Reconnecting...")
            #     # Retry connection
            #     asyncio.create_task(connect_to_cadence_sensor(websocket))
        else:
            print("Action field is missing or its value is not 'statuscheck'.")
    except json.JSONDecodeError:
        print("Message not in JSON format.")

async def websocket_message_handler(websocket):
    """Handle incoming messages from the WebSocket server."""
    try:
        async for message in websocket:
            await handle_server_message(message, websocket)
    except websockets.ConnectionClosedError:
        print("WebSocket connection closed.")
    except Exception as e:
        print(f"Error handling WebSocket message: {e}")

async def discover_ble_device():
    """Scan for BLE devices."""
    print("Scanning for BLE devices...")
    devices = await BleakScanner.discover()
    for device in devices:
        print(f"Found device: {device}")

async def handle_ble_notifications(client, websocket):
    """Handle notifications from the BLE device."""
    try:
        def csc_measurement_handler(data):
            try:
                data = { 
                        "type": "bike",
                        "action" : "data",
                        "cumulative_crank_revs" :data.cumulative_crank_revs, 
                        "last_crank_event_time" :data.last_crank_event_time
                    }

                # Convert dictionary to JSON string
                data_str = json.dumps(data)
                print("Sending data to WebSocket server:", data_str)
                asyncio.create_task(send_data_via_websocket(websocket, data_str))
            except Exception as e:
                print(f"Error handling CSC data: {e}")

        csc_service = CyclingSpeedCadenceService(client)
        csc_service.set_csc_measurement_handler(csc_measurement_handler)
        await csc_service.enable_csc_measurement_notifications()

        while True:
            await asyncio.sleep(1)

    except Exception as e:
        print(f"Error in BLE notification handler: {e}")

async def connect_to_cadence_sensor(websocket):
    """Connect to the cadence sensor and handle notifications."""
    global client  # Declare client as global to modify it within this function
    while True:
        try:
            print("Attempting to connect to BLE device...")
            client = BleakClient(device_address)  # Assign client inside the try block
            await client.connect()

            if client.is_connected:
                print("Connected to BLE device.")
                await handle_ble_notifications(client, websocket)
            else:
                print("Failed to connect to BLE device.")
        except Exception as e:
            print(f"Cadence sensor connection error: {e}")
            await asyncio.sleep(2)  # Retry every 2 seconds
            print("Retry connection to the cadence sensor...")
            # if client and client.is_connected:
            #     await client.disconnect()  # Ensure client is properly closed before retrying
            #     client = None
            data = { 
                        "type": "bike",
                        "message" : "Cadence Sensor Offline",
                    }

                # Convert dictionary to JSON string
            data_str = json.dumps(data)
            await send_data_via_websocket(websocket, data_str)
        # finally:
        #     if client and client.is_connected:
        #         await client.disconnect()  # Ensure client is properly closed before retrying
        #         client = None

async def connect_to_websocket():
    """Connect to the WebSocket server."""
    while True:
        try:
            async with websockets.connect(WEBSOCKET_SERVER_URI, ping_timeout=None) as websocket:
                print("Connected to WebSocket server.")
                websocket_task = asyncio.create_task(websocket_message_handler(websocket))
                cadence_task = asyncio.create_task(connect_to_cadence_sensor(websocket))

                await asyncio.gather(websocket_task, cadence_task)
        except Exception as e:
            print(f"Error connecting to WebSocket server: {e}")
            print("Retrying connection in 10 seconds...")
            await asyncio.sleep(10)

async def main():
    """Main function."""
    os.system(f'title {title}')
    await discover_ble_device()
    while True:
        await connect_to_websocket()

if __name__ == "__main__":
    asyncio.run(main())
