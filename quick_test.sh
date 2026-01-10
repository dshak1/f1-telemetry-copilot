#!/bin/bash
# Quick test - run for 30 seconds then kill

cd /Users/diarshakimov/Downloads/f1-telemetry-copilot

# Auto-select Verstappen (driver 4) and skip strategy prompt
echo -e "n\n4\n\n" | bash run_farvis_demo.sh &

PID=$!
sleep 45
kill $PID 2>/dev/null
wait $PID 2>/dev/null

echo ""
echo "=========================================="
echo "Demo complete - integration test finished"
echo "=========================================="
