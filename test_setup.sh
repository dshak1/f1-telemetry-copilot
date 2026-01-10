#!/bin/bash

# Quick test script to verify FARVIS is ready for demo

echo "🏎️  FARVIS Pre-Demo Test Suite"
echo "================================"
echo ""

# Test 1: Check C++ compiler
echo "Test 1: Checking C++ compiler..."
if command -v g++ &> /dev/null; then
    VERSION=$(g++ --version | head -n1)
    echo "✅ g++ found: $VERSION"
else
    echo "❌ g++ not found. Install with: brew install gcc"
    exit 1
fi

# Test 2: Check Python
echo ""
echo "Test 2: Checking Python..."
if command -v python3 &> /dev/null; then
    VERSION=$(python3 --version)
    echo "✅ Python found: $VERSION"
else
    echo "❌ Python 3 not found. Install from python.org"
    exit 1
fi

# Test 3: Compile traditional mode
echo ""
echo "Test 3: Compiling traditional mode..."
if g++ -std=c++17 -I src \
    src/main.cpp \
    src/telemetry/TelemetryGenerator.cpp \
    src/strategy/RaceSimulator.cpp \
    src/strategy/StrategyAnalyzer.cpp \
    src/race-control/TrackLimitsMonitor.cpp \
    src/race-control/PenaltyEnforcer.cpp \
    -o f1-telemetry \
    -pthread 2>/dev/null; then
    echo "✅ Traditional mode compiled successfully"
    rm -f f1-telemetry
else
    echo "❌ Traditional mode compilation failed"
    echo "   Try running: bash run_traditional.sh"
    exit 1
fi

# Test 4: Compile Gemini mode
echo ""
echo "Test 4: Compiling Gemini mode..."
if g++ -std=c++17 -I src \
    src/main_gemini.cpp \
    src/telemetry/TelemetryGenerator.cpp \
    src/strategy/RaceSimulator.cpp \
    src/strategy/StrategyAnalyzer.cpp \
    src/race-control/TrackLimitsMonitor.cpp \
    src/race-control/PenaltyEnforcer.cpp \
    -o f1-telemetry-gemini \
    -pthread 2>/dev/null; then
    echo "✅ Gemini mode compiled successfully"
    rm -f f1-telemetry-gemini
else
    echo "❌ Gemini mode compilation failed"
    echo "   Check src/main_gemini.cpp for errors"
    exit 1
fi

# Test 5: Check Python dependencies
echo ""
echo "Test 5: Checking Python environment..."
if [ -d "venv" ]; then
    echo "✅ Virtual environment exists"
else
    echo "⚠️  No virtual environment found (will be created on first run)"
fi

# Test 6: Check for API key
echo ""
echo "Test 6: Checking Gemini API key..."
if [ -f ".env" ]; then
    if grep -q "GEMINI_API_KEY" .env; then
        echo "✅ .env file exists with API key"
    else
        echo "⚠️  .env exists but no API key found"
        echo "   Demo will run in MOCK MODE"
    fi
else
    echo "⚠️  No .env file found"
    echo "   Copy .env.example to .env and add your key"
    echo "   Demo will run in MOCK MODE (still works!)"
fi

# Test 7: Check scripts are executable
echo ""
echo "Test 7: Checking script permissions..."
if [ -x "run_farvis_demo.sh" ]; then
    echo "✅ run_farvis_demo.sh is executable"
else
    echo "⚠️  Making run_farvis_demo.sh executable..."
    chmod +x run_farvis_demo.sh
fi

if [ -x "run_traditional.sh" ]; then
    echo "✅ run_traditional.sh is executable"
else
    echo "⚠️  Making run_traditional.sh executable..."
    chmod +x run_traditional.sh
fi

# Summary
echo ""
echo "================================"
echo "📊 Test Summary"
echo "================================"
echo ""
echo "✅ All critical tests passed!"
echo ""
echo "Next steps:"
echo "1. Test traditional mode: bash run_traditional.sh"
echo "2. Test Gemini mode: bash run_farvis_demo.sh"
echo "3. Record demo video"
echo "4. Submit to Devpost"
echo ""
echo "🏁 Ready to race! Good luck! 🏎️"
