#!/bin/bash
echo "Waiting for quota reset (60 seconds)..."
sleep 60
echo "Testing API..."
python3 test_api_final.py
