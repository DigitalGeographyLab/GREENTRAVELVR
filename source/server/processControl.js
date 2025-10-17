// scriptHandler.js
// This file is experimental. This code is an attempt to restart the candence client terminal from the dashboard button.
import { spawn, exec } from 'child_process';

let pythonProcess = null;
let pythonProcessPid = null; // To track the actual Python process PID

export function handleScriptMessages(ws, message) {
    if (message.action === 'start') {
        if (pythonProcess === null) {
            pythonProcess = spawn('cmd.exe', ['/c', 'start', 'cmd.exe', '/k', 'python ..client/bike/BikeDataToServer.py'], {
                detached: true,
                stdio: 'ignore'
            });

            // Capture the actual PID of the Python process
            setTimeout(() => {
                exec(`wmic process where "ParentProcessId=${pythonProcess.pid}" get ProcessId`, (error, stdout, stderr) => {
                    if (error) {
                        console.error(`Error getting child process PID: ${error.message}`);
                        ws.send(JSON.stringify({ type: 'bike', processstate: 'error', message: error.message }));
                    } else {
                        const pids = stdout.split('\n').map(line => line.trim()).filter(line => line && !isNaN(line));
                        if (pids.length > 0) {
                            pythonProcessPid = pids[0]; // Assuming the first PID is the correct one
                            ws.send(JSON.stringify({ type: 'bike', processstate: 'started', pid: pythonProcessPid }));
                        } else {
                            console.error('No child process PID found.');
                            ws.send(JSON.stringify({ type: 'bike', processstate: 'error', message: 'No child process PID found.' }));
                        }
                    }
                });
            }, 1000); // Delay to allow the Python process to start
        } else {
            ws.send(JSON.stringify({ type: 'bike', status: 'already running', pid: pythonProcessPid }));
        }
    } else if (message.action === 'stop') {
        if (pythonProcessPid !== null) {
            try {
                exec(`taskkill /pid ${pythonProcessPid} /f /t`, (error, stdout, stderr) => {
                    if (error) {
                        console.error(`Error stopping the script: ${error.message}`);
                        ws.send(JSON.stringify({ type: 'bike', processstate: 'error', message: error.message }));
                    } else {
                        console.log(`Script stopped successfully: ${stdout}`);
                        ws.send(JSON.stringify({ type: 'bike', processstate: 'stopped' }));
                        pythonProcess = null;
                        pythonProcessPid = null;
                    }
                });
            } catch (error) {
                console.error('Error stopping the script:', error);
                ws.send(JSON.stringify({ type: 'bike', processstate: 'error', message: error.message }));
            }
        } else {
            ws.send(JSON.stringify({ type: 'bike', processstate: 'not running' }));
        }
    } else if (message.action === 'processstate') {
        if (pythonProcessPid !== null) {
            ws.send(JSON.stringify({ type: 'bike', processstate: 'running', pid: pythonProcessPid }));
        } else {
            ws.send(JSON.stringify({ type: 'bike', processstate: 'not running' }));
        }
    } else {
        console.log(`Unknown script action: ${message.action}`);
    }
}
