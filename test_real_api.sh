#!/bin/bash
# Quick FARVIS test with real Gemini API

cd /Users/diarshakimov/Downloads/f1-telemetry-copilot

# Auto-select Verstappen (driver 4)
(echo "n"; echo "4"; echo ""; sleep 80; killall f1-telemetry-gemini) | bash run_farvis_demo.sh 2>&1

echo ""
echo "=========================================="
echo "Demo complete!"
echo "=========================================="
