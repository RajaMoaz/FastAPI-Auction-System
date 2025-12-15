import io from 'socket.io-client';
import type { Socket } from './types/socketio.d'; 

// CRITICAL: The URL MUST match where your FastAPI backend is running.
const SOCKET_SERVER_URL = 'http://127.0.0.1:8000';

// ULTIMATE FIX: Explicitly set path, force WebSocket, and DISABLE UPGRADE to stop fallback spam.
const socket: Socket = io(SOCKET_SERVER_URL, {
    path: '/ws/socket.io', // <--- FIX: Must include the '/ws' prefix
    transports: ['websocket'], // Force WebSocket transport
    upgrade: false // <--- FIX: Prevents the client from spamming the wrong path
});

// Basic connection logs
socket.on('connect', () => {
    console.log("Socket.IO client connected successfully! Connection ID:", socket.id);
});

socket.on('disconnect', () => {
    console.log("Socket.IO disconnected.");
});

// Example of listening for a specific event from the server
socket.on('new_bid', (data) => {
    console.log('Received new bid:', data);
    // The component using this socket will consume this event
});

export default socket;
