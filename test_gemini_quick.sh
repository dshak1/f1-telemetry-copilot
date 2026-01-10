#!/bin/bash

# Quick Gemini API test before running full demo

echo "🏎️  FARVIS - Quick Gemini API Test"
echo "===================================="
echo ""

# Check .env exists
if [ ! -f ".env" ]; then
    echo "❌ .env file not found"
    exit 1
fi

# Test Gemini API
echo "Testing Gemini API connection..."
python3 test_gemini.py 2>&1 | tail -20

echo ""
echo "===================================="
echo "If you see strategy output above, Gemini is ready!"
echo ""
echo "Free tier limits:"
echo "  • 15 requests per minute"
echo "  • 1500 requests per day"
echo "  • FARVIS calls every 5 seconds = ~12 RPM (under limit!)"
echo ""
echo "Ready to run full demo? bash run_farvis_demo.sh"
