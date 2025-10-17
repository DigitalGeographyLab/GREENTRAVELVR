import WebSocket, { WebSocketServer } from 'ws';
import { randomUUID } from 'crypto';
import { handleScriptMessages } from './processControl.js';
import { exec } from 'child_process';

const title = "GVTL NODE SERVER";

const clients = new Map(); // has to be a Map instead of {} due to non-string keys
const wss = new WebSocketServer({ port: 8080 }); // initiate a new server that listens on port 8080

// set up event handlers and do other things upon a client connecting to the server
wss.on('connection', (ws) => {
    // create an id to track the client
    const id = randomUUID();
    clients.set(ws, id);
    console.log(`new connection assigned id: ${id}`);

    // send the id back to the newly connected client
    ws.send(`You have been assigned id ${id}`);

    ws.on('message', (data) => {
        try {
            const message = JSON.parse(data);
            if (message.type === 'bikescriptaction') {
                handleScriptMessages(ws, message);
            }
        } catch (error) {
            // console.log('Incoming data is not JSON:', data);
            // Handle non-JSON data, if needed
            // Example: Logging the data as is
            console.log(`Non-JSON data received from client ${clients.get(ws)}: ${data}`);
        }

        console.log(`Data received from client ${clients.get(ws)}: ${data}`);
        const message_string = `${data}`; // This is important. Don't send the data as is.
        serverBroadcastExceptSender(message_string, ws);

    });

    // stop tracking the client upon that client closing the connection
    ws.on('close', () => {
        console.log(`connection (id = ${clients.get(ws)}) closed`);
        clients.delete(ws);
    });
});

// send a message to all the connected clients about how many of them there are every 15 seconds
setInterval(() => {
    console.log(`Number of connected clients: ${clients.size}`);
}, 5000);

// function for sending a message to every connected client except the sender
function serverBroadcastExceptSender(message, sender) {
    wss.clients.forEach((client) => {
        if (client !== sender && client.readyState === WebSocket.OPEN) {
        // if (client.readyState === WebSocket.OPEN) {
            client.send(message);
        }
    });
}

// Set the command line window title
exec('title ' + title);
console.log('The server is running and waiting for connections');
