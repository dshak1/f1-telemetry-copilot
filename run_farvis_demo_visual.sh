#!/bin/bash
# FARVIS Demo - Shows telemetry leaderboard AND Gemini strategic output

cd /Users/diarshakimov/Downloads/f1-telemetry-copilot

echo "FARVIS - F1 Race Engineer AI Copilot"
echo "=========================================="
echo ""
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

# Check for API key
if [ -f ".env" ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

echo "Starting FARVIS demo..."
echo "- C++ shows real-time race telemetry (all 20 drivers)"
echo "- Gemini provides strategic guidance for your chosen driver"
echo "- [AI] marker shows which driver FARVIS is coaching"
echo ""
echo "Press Ctrl+C to stop"
echo ""

# Run with FARVIS mode enabled
export FARVIS_GEMINI_MODE=1

# Start both components
# C++ outputs: stderr=telemetry display, stdout=JSON
# Python reads JSON from stdin and outputs strategy
./f1-telemetry-gemini 2>&1 | python3 gemini_race_engineer.py
