#!/bin/bash

# Debug script to check what's using the ports
echo "🔍 Debugging port usage..."
echo ""

echo "📊 Processes using port 8000:"
lsof -i :8000 2>/dev/null || echo "No processes found on port 8000"
echo ""

echo "📊 Processes using port 5173:"
lsof -i :5173 2>/dev/null || echo "No processes found on port 5173"
echo ""

echo "📊 All Python processes:"
ps aux | grep python | grep -v grep
echo ""

echo "📊 All Node processes:"
ps aux | grep node | grep -v grep
echo ""

echo "📊 All processes with 'main.py' or 'vite':"
ps aux | grep -E "(main\.py|vite)" | grep -v grep
echo ""

echo "🧹 Want to kill all processes? Run:"
echo "  Kill port 8000: lsof -t -i:8000 | xargs kill -9"
echo "  Kill port 5173: lsof -t -i:5173 | xargs kill -9"
