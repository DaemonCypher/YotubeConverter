#!/bin/bash

# Start FastAPI backend
uvicorn app:app --host=0.0.0.0 --port=8080 &

# Wait for FastAPI backend to start
sleep 5

# Change directory to Vue.js frontend
cd YoutubeConverter

# Start Vue.js frontend
npm run serve

