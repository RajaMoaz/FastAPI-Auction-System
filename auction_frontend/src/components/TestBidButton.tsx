// src/components/TestBidButton.tsx
'use client'; // CRITICAL: Marks this as a Client Component

import React from 'react';

// The URL should match the endpoint you defined in your backend (FastAPI)
const BID_API_URL = 'http://localhost:8000/bid/auction_123';

const TestBidButton: React.FC = () => {
    const submitTestBid = async () => {
        try {
            const testBidData = {
                bidder_id: "test_user_123",
                new_amount: Math.floor(Math.random() * 100) + 100, // Random amount
            };

            // This calls the FastAPI endpoint: POST /bid/{auction_id}
            const response = await fetch(BID_API_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(testBidData),
            });

            if (response.ok) {
                console.log("Test bid submitted successfully.");
            } else {
                console.error("Failed to submit test bid. Status:", response.status);
            }
        } catch (error) {
            console.error("API call error:", error);
        }
    };

    return (
        <button
            onClick={submitTestBid} // This is the interactive handler, now safe in a Client Component
            className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded transition duration-150 ease-in-out"
        >
            Send Test Bid (API POST)
        </button>
    );
};

export default TestBidButton;