#!/bin/bash
# OmniRec — Standalone Startup Launcher Script

echo "============================================================"
echo " Starting OmniRec Platform Services (Native Local Mode)"
echo "============================================================"

# 1. Start Python FastAPI AI Recommendation Microservice (Port 8000)
echo "[1/3] Launching Python FastAPI AI Engine on port 8000..."
cd ai-service
python3 main.py &
AI_PID=$!
cd ..

# 2. Start React Frontend Server (Port 5173)
echo "[2/3] Launching React Vite Frontend on port 5173..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo "------------------------------------------------------------"
echo " OmniRec Frontend: http://localhost:5173"
echo " Python AI Service: http://localhost:8000/docs"
echo " Spring Boot API:   http://localhost:8080/swagger-ui.html"
echo "------------------------------------------------------------"

trap "kill $AI_PID $FRONTEND_PID" EXIT
wait
