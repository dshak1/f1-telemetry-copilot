#!/bin/bash

# Quick test of FARVIS with driver selection

echo "🏎️  Testing FARVIS Driver Selection"
echo "===================================="
echo ""

export FARVIS_GEMINI_MODE=1

# Auto-select Verstappen (driver 0) for quick test
echo "n
0
" | ./f1-telemetry-gemini 2>&1 | head -100
