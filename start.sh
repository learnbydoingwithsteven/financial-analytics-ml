#!/bin/bash

echo "===================================="
echo "Financial Analytics Dashboard"
echo "===================================="
echo ""

echo "Starting Backend Server..."
cd backend
python main.py &
BACKEND_PID=$!
cd ..

echo "Waiting for backend to start..."
sleep 5

echo "Starting Frontend Server..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "===================================="
echo "Dashboard is running!"
echo "Backend: http://localhost:8000"
echo "Frontend: http://localhost:5173"
echo "===================================="
echo ""
echo "Press Ctrl+C to stop all servers"

# Wait for user interrupt
trap "echo 'Stopping servers...'; kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait
