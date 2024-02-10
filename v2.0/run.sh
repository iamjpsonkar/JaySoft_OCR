#!/bin/bash

# Define log file paths
BACKEND_LOG="backend.log"
FRONTEND_LOG="frontend.log"

# Clear log files
truncate -s 0 "$BACKEND_LOG"
truncate -s 0 "$FRONTEND_LOG"

# Run backend
cd backend
python -m app 2>&1 | tee "../$BACKEND_LOG" &

# Wait for backend to start
sleep 5

# Run frontend
cd ../ocr
npm start dev 2>&1 | tee "../../$FRONTEND_LOG"
