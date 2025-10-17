/* 
  JSON structure between server and other apps is known. Strings used in following code are adhering to that structure.
  For more details: 
  https://github.com/DigitalGeographyLab/UE5-Biopac-Cadence-NetworkController/blob/main/README.md
*/

const APPS = {
    BIKE: 'bike',
    UE5: 'ue5',
    BIOPAC: 'biopac',
    DASHBOARD: 'dashboard',
    SERVER: 'server'
  };
  
  const STATUS = {
    CONNECTED: 'connected',
    DISCONNECTED: 'disconnected',
    LIVE_DATA: 'live_data',
    ERROR: 'error',
    DEFAULT: 'default'
  };
  
  const SOCKET_URL = 'ws://localhost:8080';
  const STATUSCHECK_INTERVAL = 10000;
  
  let socket = null;
  
  // Function to update the status of any icon (Server or App)
  function updateStatus(elementId, status, isBlinking = false) {
    const element = document.getElementById(elementId+'SVG');
    element.classList.remove('text-red-500', 'text-green-500', 'blinking');
    if (status === STATUS.CONNECTED || status === STATUS.LIVE_DATA) {
      element.classList.add('text-green-500');
      if (isBlinking) {
        element.classList.add('blinking');
      }
    } else {
      element.classList.add('text-red-500');
    }
  }
  
  // Function to handle WebSocket connection
  function connectWebSocket() {
    socket = new WebSocket(SOCKET_URL);
  
    socket.onopen = () => handleSocketOpen();
    socket.onmessage = (event) => handleSocketMessage(event);
    socket.onclose = () => handleSocketClose();
    socket.onerror = () => handleSocketError();
  }
  
  // Event handler: WebSocket connection opened
  function handleSocketOpen() {
    updateStatus(APPS.SERVER, STATUS.CONNECTED);
    sendStatusCheck();
  }
  
  // Event handler: WebSocket message received
  function handleSocketMessage(event) {
    try {
      const data = JSON.parse(event.data);
      console.log('Message received:', data);
  
      switch (data.type) {
        case APPS.DASHBOARD:
          updateStatus(APPS.SERVER, STATUS.CONNECTED);
          break;
        case APPS.BIKE:
          const bikeStatus = data.action === 'data' ? STATUS.LIVE_DATA : STATUS.CONNECTED;
          updateStatus(APPS.BIKE, bikeStatus, bikeStatus === STATUS.LIVE_DATA);
          break;
        case APPS.UE5:
          updateStatus(APPS.UE5, STATUS.CONNECTED);
          break;
        case APPS.BIOPAC:
          updateStatus(APPS.BIOPAC, STATUS.CONNECTED);
          break;
        default:
          console.log('Unknown app type:', data.type);
      }
    } catch (error) {
      console.error('Error parsing message:', error);
    }
  }
  
  // Event handler: WebSocket connection closed
  function handleSocketClose() {
    updateStatus(APP.SERVER, STATUS.DISCONNECTED);
    updateAppStatuses(STATUS.DISCONNECTED);
    socket = null;
  }
  
  // Event handler: WebSocket connection error
  function handleSocketError() {
    console.error('WebSocket error');
    updateStatus(APP.SERVER, STATUS.ERROR);
    updateAppStatuses(STATUS.ERROR);
  }
  
  // Function to send status check request
  function sendStatusCheck() {
    if (socket) {
      socket.send(JSON.stringify({ type: APPS.DASHBOARD, action: 'statuscheck' }));
    }
  }
  
  // Function to update all application statuses to a given state
  function updateAppStatuses(status) {
    updateStatus(APPS.BIKE, status);
    updateStatus(APPS.UE5, status);
    updateStatus(APPS.BIOPAC, status);
  }
  
  // Function to check server and application statuses
  function checkStatuses() {
    console.log('Checking statuses...');
    updateAppStatuses(STATUS.DEFAULT);
  
    if (!socket) {
      connectWebSocket();
    } else {
      sendStatusCheck();
    }
  }
  
  // Script control functions
  function restartCadenceScript() {
    sendScriptAction('start');
  }
  
  function stopScript() {
    sendScriptAction('stop');
  }
  
  function sendScriptAction(action) {
    if (socket) {
      socket.send(JSON.stringify({ type: 'bikescriptaction', action }));
    }
  }
  
  // Start periodic status check
  setInterval(checkStatuses, STATUSCHECK_INTERVAL);
  