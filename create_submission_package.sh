#!/bin/bash

# FARVIS Submission Package Generator

echo "🏁 FARVIS Submission Package Generator"
echo "======================================"
echo ""

# Create submission directory
SUBMIT_DIR="farvis_submission_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$SUBMIT_DIR"

echo "📦 Creating submission package in: $SUBMIT_DIR"
echo ""

# Copy key documentation files
echo "📄 Copying documentation..."
cp README_NEW.md "$SUBMIT_DIR/README.md"
cp DEVPOST_SUBMISSION.md "$SUBMIT_DIR/"
cp DEMO_SCRIPT.md "$SUBMIT_DIR/"
cp IMPLEMENTATION_CHECKLIST.md "$SUBMIT_DIR/"
cp .env.example "$SUBMIT_DIR/"
cp requirements.txt "$SUBMIT_DIR/"

# Copy scripts
echo "🔧 Copying scripts..."
cp run_farvis_demo.sh "$SUBMIT_DIR/"
cp run_traditional.sh "$SUBMIT_DIR/"
cp test_setup.sh "$SUBMIT_DIR/"
cp gemini_race_engineer.py "$SUBMIT_DIR/"

# Copy source code
echo "💻 Copying source code..."
cp -r src "$SUBMIT_DIR/"

# Create a quick setup guide
cat > "$SUBMIT_DIR/QUICK_START.txt" << 'EOF'
FARVIS - Quick Start Guide
==========================

1. VERIFY EVERYTHING WORKS:
   ./test_setup.sh

2. RUN TRADITIONAL MODE (No AI):
   bash run_traditional.sh
   
3. RUN FARVIS MODE (With Gemini):
   bash run_farvis_demo.sh
   
4. TO USE REAL GEMINI API:
   cp .env.example .env
   # Edit .env and add GEMINI_API_KEY
   bash run_farvis_demo.sh

For full documentation, see README.md
For judge presentation, see DEMO_SCRIPT.md
For Devpost submission, see DEVPOST_SUBMISSION.md
EOF

# Create project info file
cat > "$SUBMIT_DIR/PROJECT_INFO.txt" << 'EOF'
FARVIS - F1 Race Engineer AI Copilot
=====================================

Tagline: Every great leader has a great #2. This is JARVIS for F1 drivers.

Technologies:
- C++17 (real-time telemetry, multithreading)
- Python 3 (integration layer)
- Google Gemini 2.0 Flash (strategic AI)

Features:
- 50Hz real-time F1 race simulation (20 drivers)
- Thread-safe producer-consumer architecture
- Realistic tire degradation and fuel modeling
- Track limits monitoring and penalty enforcement
- Gemini AI strategic guidance at lap-scale
- Event-driven API calls with smart throttling
- Multi-option strategic recommendations
- Mock mode for demo reliability

Awards Targeting:
- Best Use of Gemini API
- Lone Wanderer Award (Solo Hacker)

Key Differentiators:
- Two-layer "fast + slow AI" architecture
- Production-quality C++ with thread safety
- Realistic F1 domain modeling
- Honest framing (not claiming unrealistic AI capabilities)
- Clear value proposition for sim racing community

Contact: [Your contact info]
GitHub: [Your repo URL]
Demo Video: [Your video URL]
EOF

# Take a quick inventory
echo ""
echo "📊 Package Contents:"
echo "-------------------"
ls -1 "$SUBMIT_DIR" | while read file; do
    echo "  ✓ $file"
done

# Count lines of code
if command -v cloc &> /dev/null; then
    echo ""
    echo "📈 Code Statistics:"
    echo "-------------------"
    cloc --quiet "$SUBMIT_DIR/src" "$SUBMIT_DIR/gemini_race_engineer.py" 2>/dev/null || echo "  (install 'cloc' for detailed stats)"
else
    CPP_LINES=$(find "$SUBMIT_DIR/src" -name "*.cpp" -o -name "*.h" | xargs wc -l 2>/dev/null | tail -1 | awk '{print $1}')
    PY_LINES=$(wc -l "$SUBMIT_DIR/gemini_race_engineer.py" 2>/dev/null | awk '{print $1}')
    echo "  C++ code: ~$CPP_LINES lines"
    echo "  Python code: ~$PY_LINES lines"
fi

# Create a zip archive
echo ""
echo "📦 Creating ZIP archive..."
zip -r "${SUBMIT_DIR}.zip" "$SUBMIT_DIR" > /dev/null 2>&1

if [ -f "${SUBMIT_DIR}.zip" ]; then
    SIZE=$(du -h "${SUBMIT_DIR}.zip" | cut -f1)
    echo "✅ Created: ${SUBMIT_DIR}.zip ($SIZE)"
else
    echo "⚠️  ZIP creation failed, but directory is ready"
fi

echo ""
echo "✅ Submission package ready!"
echo ""
echo "📋 Next Steps:"
echo "1. Review files in $SUBMIT_DIR/"
echo "2. Record demo video (see DEMO_SCRIPT.md)"
echo "3. Take screenshots while running demo"
echo "4. Fill out Devpost form (see DEVPOST_SUBMISSION.md)"
echo "5. Upload ${SUBMIT_DIR}.zip or push to GitHub"
echo "6. Submit before deadline!"
echo ""
echo "🏁 Good luck! You got this! 🏎️"
