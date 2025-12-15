// src/components/SocketTest.tsx
'use client'; 

import React, { useEffect, useState, useCallback } from 'react';
import io from 'socket.io-client'; 

let socket: any | null = null; 

// FIX 1: The incoming bid amount is a STRING from the Python backend.
interface BidData {
    auctionId: string;
    newBid: string; 
    bidderId: string;
}

const SOCKET_SERVER_URL = 'http://127.0.0.1:8000';
const API_URL = 'http://127.0.0.1:8000/api/test-bid';


const SocketTest: React.FC = () => {
    const [isConnected, setIsConnected] = useState(false);
    const [latestBid, setLatestBid] = useState<BidData | null>(null); 
    const [loading, setLoading] = useState(false);

    const submitTestBid = useCallback(async () => {
        setLoading(true);
        try {
            const response = await fetch(API_URL, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: "Trigger Bid" }),
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

        } catch (error) {
            console.error('Error submitting test bid:', error);
            alert('Failed to submit test bid. Check if the backend is running correctly.');
        } finally {
            setLoading(false);
        }
    }, []);

    useEffect(() => {
        if (!socket) {
            // FIX 2 & 3: Re-adding the critical connection options
            socket = io(SOCKET_SERVER_URL, {
                path: '/ws/socket.io', // <-- FIX: Use the correct backend path
                transports: ['websocket'],
                upgrade: false // <-- FIX: Stop the client from spamming wrong paths
            });

            socket.on('connect', () => {
                console.log('Socket.IO Connected!');
                setIsConnected(true);
            });

            socket.on('disconnect', () => {
                console.log('Socket.IO Disconnected.');
                setIsConnected(false);
            });

            socket.on('new_bid', (data: BidData) => {
                console.log('--- RECEIVED NEW BID ---', data);
                setLatestBid(data);
            });

            return () => {
                if (socket) {
                    socket.disconnect(); 
                    socket = null; 
                }
            };
        }
    }, []); 

    return (
        <div className="p-8 border rounded-lg shadow-2xl bg-white w-full max-w-lg space-y-4">
            <h2 className="text-2xl font-extrabold mb-4 text-center text-indigo-700">Real-Time Auction Test</h2>
            
            {/* Status Section */}
            <div className="p-3 border rounded">
                <p className={`text-lg font-semibold ${isConnected ? 'text-green-600' : 'text-red-600'} flex justify-between items-center`}>
                    Connection Status:
                    <span className="font-bold">
                        {isConnected ? 'LIVE' : 'DISCONNECTED'}
                    </span>
                </p>
            </div>

            {/* Test Button Section */}
            <button
                onClick={submitTestBid}
                disabled={!isConnected || loading}
                className={`w-full py-3 px-4 rounded-lg text-white font-bold transition duration-300 ${
                    !isConnected || loading
                        ? 'bg-gray-400 cursor-not-allowed'
                        : 'bg-indigo-600 hover:bg-indigo-700 shadow-md'
                }`}
            >
                {loading ? 'Sending...' : 'Send Test Bid (API POST)'}
            </button>

            {/* Received Data Section */}
            <h3 className="text-xl font-semibold pt-4 text-gray-700 border-t">Latest Broadcasted Bid:</h3>
            {latestBid ? (
                <div className="mt-2 p-4 bg-yellow-50 border-l-4 border-yellow-500 rounded space-y-1">
                    <p><strong>Auction ID:</strong> {latestBid.auctionId}</p>
                    <p><strong>New Bid Amount:</strong> <span className="text-xl font-extrabold text-green-700">$
                        {/* FIX 4: Convert string to float before using .toFixed() to prevent crash */}
                        {parseFloat(latestBid.newBid).toFixed(2)}
                    </span></p>
                    <p><strong>Bidder ID:</strong> {latestBid.bidderId}</p>
                </div>
            ) : (
                <p className="text-gray-500 mt-2 p-4 bg-gray-50 rounded">Click the button above to start receiving bids.</p>
            )}
        </div>
    );
};

export default SocketTest;