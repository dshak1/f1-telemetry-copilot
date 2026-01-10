#!/bin/bash

# FARVIS Demo Script - Compile and Run with Gemini Integration

set -e

echo "FARVIS - F1 Race Engineer AI Copilot"
echo "=========================================="
echo ""

# Compile C++ telemetry system
echo "Compiling C++ telemetry system..."
g++ -std=c++17 -I src \
    src/main_gemini.cpp \
    src/telemetry/TelemetryGenerator.cpp \
    src/strategy/RaceSimulator.cpp \
    src/strategy/StrategyAnalyzer.cpp \
    src/race-control/TrackLimitsMonitor.cpp \
    src/race-control/PenaltyEnforcer.cpp \
    -o f1-telemetry-gemini \
    -pthread

echo "Compilation successful!"
echo ""

# Check if Python environment is set up
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

echo "Installing Python dependencies..."
source venv/bin/activate
pip install -q --upgrade pip
pip install -q -r requirements.txt

echo "Python environment ready!"
echo ""

# Check for API key
if [ -f ".env" ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

if [ -z "$GEMINI_API_KEY" ]; then
    echo "WARNING: GEMINI_API_KEY not set"
    echo "   Get your key from: https://aistudio.google.com/app/apikey"
    echo "   Add it to .env file (see .env.example)"
    echo "   Running in MOCK MODE (simulated AI responses)"
    echo ""
fi

echo "Starting FARVIS demo..."
echo "   - C++ telemetry outputs JSON to stdout"
echo "   - Python race engineer reads JSON and provides strategy"
echo "   - Press Ctrl+C to stop"
echo ""
echo "─────────────────────────────────────────"
echo ""

# Run with piped output
# C++ writes normal output to stderr, JSON to stdout
# Python reads JSON from stdin
export FARVIS_GEMINI_MODE=1
echo "n" | ./f1-telemetry-gemini 2>&1 | python3 gemini_race_engineer.py
