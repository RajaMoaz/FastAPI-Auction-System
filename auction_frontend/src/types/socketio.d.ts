// src/types/socketio.d.ts

// Define the Socket type as a local module interface.
export interface Socket {
    connected: boolean;
    on(eventName: string, listener: (...args: any[]) => void): void;
    off(eventName: string, listener: (...args: any[]) => void): void;
    emit(eventName: string, ...args: any[]): void;
    [key: string]: any;
}

// Dummy export to make it a module
export {};
