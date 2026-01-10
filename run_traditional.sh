#!/bin/bash

# Quick compile and run traditional mode (no Gemini)

echo "🏎️  Compiling F1 Telemetry System..."

g++ -std=c++17 -I src \
    src/main.cpp \
    src/telemetry/TelemetryGenerator.cpp \
    src/strategy/RaceSimulator.cpp \
    src/strategy/StrategyAnalyzer.cpp \
    src/race-control/TrackLimitsMonitor.cpp \
    src/race-control/PenaltyEnforcer.cpp \
    -o f1-telemetry \
    -pthread

echo "✅ Compilation successful!"
echo ""
echo "🏁 Starting race simulation..."
echo ""

./f1-telemetry
