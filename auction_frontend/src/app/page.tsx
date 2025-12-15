// src/app/page.tsx
import SocketTest from '@/components/SocketTest';
import TestBidButton from '@/components/TestBidButton'; // <-- NEW IMPORT

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24 bg-gray-50">
      <div className="z-10 w-full max-w-5xl items-center justify-between font-mono text-sm lg:flex">
        <h1 className="text-2xl font-bold text-gray-800">Auction System Frontend</h1>
      </div>

      <div className="mt-10 w-full max-w-5xl">
        {/* Real-time component */}
        <SocketTest /> 
      </div>

      {/* Test Section for Sending Bids - REMAINS a Server Component wrapper */}
      <div className="mt-8">
        <h3 className="text-lg font-semibold mb-4">Test Bid Submission:</h3>
        <p className="text-sm text-gray-600 mb-2">
            Click this button to trigger the API endpoint in your backend, which should send a 'new_bid' event.
        </p>
        {/* Client Component is rendered here */}
        <TestBidButton /> 
      </div>
    </main>
  );
}

// 🛑 TestBidButton is now removed from here!