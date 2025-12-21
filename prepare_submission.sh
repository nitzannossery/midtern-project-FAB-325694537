set -e

SUBMISSION_DIR="submission_midterm_financial_mcp"

echo "=== 0) Ensure minimal required folders/files exist (auto-create if missing) ==="

# 1) README
if [ ! -f README.md ]; then
  echo "⚠️ README.md missing → creating placeholder README.md"
  cat << 'EOF' > README.md
# Financial Analysis Multi-Agent System (MCP)

## Overview
This project demonstrates a Multi-Agent Control Project (MCP) system for financial analysis.

## Architecture
User → Orchestrator → (Market Data Agent, Fundamental & News Agent, Portfolio & Risk Agent) → Final Answer

## ReAct
Each agent follows a ReAct-style structure (Reason → Act → Output).

## Query Difficulty Levels
- Easy: direct alignment to retrieved market/fundamental signals.
- Medium: aggregation across multiple agents.
- Hard: metadata-driven reasoning (symbol, risk profile, horizon).
- Hard+ (Bonus): reasoning over tabular data with evidence and ground truth.

## How to Run
python3 -m pip install -r requirements.txt  
python3 -m streamlit run ui/app.py

## Evaluation
See evaluation/ground_truth.md and evaluation/screenshots/
EOF
fi

# 2) evaluation structure
mkdir -p evaluation/screenshots
if [ ! -f evaluation/ground_truth.md ]; then
  echo "⚠️ evaluation/ground_truth.md missing → creating it"
  cat << 'EOF' > evaluation/ground_truth.md
# Ground Truth for Evaluation

## Metrics
- Correctness: Answer matches ground truth.
- Faithfulness: No unsupported claims.
- Coverage: Uses all required inputs/constraints.

## Hard+ Tabular Demo (Ground Truth)
Table:
Quarter | Revenue ($M) | Net Income ($M)
Q1      | 120          | 15
Q2      | 140          | 22
Q3      | 135          | 18
Q4      | 160          | 30

Question: Which quarter has the highest net income?
Ground Truth Answer: Q4
Evidence: Q4 has net income 30 (highest).
EOF
fi

# 3) GitHub link placeholder
if [ ! -f GITHUB_LINK.txt ]; then
  echo "⚠️ GITHUB_LINK.txt missing → creating it"
  cat << 'EOF' > GITHUB_LINK.txt
Paste the GitHub repository link here.
EOF
fi

# 4) Videos presence check (cannot auto-create real recordings)
VIDEO_COUNT=$(ls *.mp4 *.mov 2>/dev/null | wc -l | tr -d ' ')
if [ "$VIDEO_COUNT" -eq 0 ]; then
  echo "⚠️ No video files found (.mp4/.mov). Creating VIDEOS_TODO.txt"
  cat << 'EOF' > VIDEOS_TODO.txt
Missing: screen recording clips.
Expected clips (you can submit as separate short videos):
- easy query
- mid-query
- hard-query
- hard1-query (Hard+)
EOF
fi

# 5) Evaluation screenshots check (cannot auto-create real screenshots)
PNG_COUNT=$(ls evaluation/screenshots/*.png 2>/dev/null | wc -l | tr -d ' ')
if [ "$PNG_COUNT" -lt 3 ]; then
  echo "⚠️ Missing evaluation screenshots (<3). Creating evaluation/screenshots/TODO.txt"
  cat << 'EOF' > evaluation/screenshots/TODO.txt
Missing screenshots for evaluation metrics (need at least 3):
- correctness.png
- faithfulness.png
- coverage.png
Place them in this folder.
EOF
fi

echo ""
echo "=== 1) Create clean submission folder ==="
rm -rf "$SUBMISSION_DIR"
mkdir -p "$SUBMISSION_DIR"

# Copy core docs
cp README.md "$SUBMISSION_DIR/"
cp GITHUB_LINK.txt "$SUBMISSION_DIR/" 2>/dev/null || true
cp evaluation/ground_truth.md "$SUBMISSION_DIR/evaluation_ground_truth.md" 2>/dev/null || true

# Copy evaluation folder
mkdir -p "$SUBMISSION_DIR/evaluation/screenshots"
cp evaluation/ground_truth.md "$SUBMISSION_DIR/evaluation/ground_truth.md"
cp -r evaluation/screenshots "$SUBMISSION_DIR/evaluation/" 2>/dev/null || true

# Copy videos (with your naming patterns)
mkdir -p "$SUBMISSION_DIR/videos"
cp *"easy query"*.mp4 *"easy query"*.mov  "$SUBMISSION_DIR/videos/" 2>/dev/null || true
cp *"mid-query"*.mp4  *"mid-query"*.mov   "$SUBMISSION_DIR/videos/" 2>/dev/null || true
cp *"hard-query"*.mp4 *"hard-query"*.mov  "$SUBMISSION_DIR/videos/" 2>/dev/null || true
cp *"hard1-query"*.mp4 *"hard1-query"*.mov "$SUBMISSION_DIR/videos/" 2>/dev/null || true

# Fallback: copy any mp4/mov if patterns didn't match
cp *.mp4 *.mov "$SUBMISSION_DIR/videos/" 2>/dev/null || true

# Add a clear video index
cat << 'EOF' > "$SUBMISSION_DIR/videos/README.txt"
Video recordings are provided as separate short clips:
- easy query   : Easy
- mid-query    : Medium
- hard-query   : Hard (metadata-driven)
- hard1-query  : Hard+ (tabular demo)

Separate clips are intentional for clarity.
EOF

# If we created TODOs, include them
cp VIDEOS_TODO.txt "$SUBMISSION_DIR/" 2>/dev/null || true

echo ""
echo "=== 2) Final verification report ==="
echo "Submission folder: $SUBMISSION_DIR"
echo ""

echo "Files:"
ls -la "$SUBMISSION_DIR" | sed -n '1,120p'

echo ""
echo "Evaluation:"
ls -la "$SUBMISSION_DIR/evaluation" || true
ls -la "$SUBMISSION_DIR/evaluation/screenshots" || true

echo ""
echo "Videos:"
ls -la "$SUBMISSION_DIR/videos" || true

echo ""
echo "=== DONE ==="
echo "If any TODO file exists inside the submission folder, complete that item before uploading."

