#!/bin/bash

# Script to save project to Git
cd "/Users/nitzannossery/Financial Analyst bot- midtern project"

echo "=== Saving project to Git ==="

# Initialize git if needed
if [ ! -d ".git" ]; then
    echo "Initializing git repository..."
    git init
fi

# Add all files
echo "Adding all files..."
git add .

# Check status
echo ""
echo "Files to be committed:"
git status --short

# Create commit
echo ""
echo "Creating commit..."
git commit -m "Complete Financial Analysis Multi-Agent System

- Implemented 3 agents (Market Data, Fundamental & News, Portfolio & Risk)
- Added Orchestrator for coordinating agents
- Built Streamlit UI with Natural Language and Form Input modes
- Added question parser and handlers for simple/complex queries
- Implemented ReAct pattern for all agents
- Added Hard+ Tabular Demo with evaluation
- Added evaluation structure and documentation
- Support for simple queries (price, market cap) and complex queries (recommendations, comparisons, portfolios)
- Robust error handling with safe formatting"

echo ""
echo "=== Commit created successfully ==="
echo ""
echo "To push to GitHub:"
echo "1. Create a repository on GitHub"
echo "2. Run: git remote add origin <your-repo-url>"
echo "3. Run: git push -u origin main"
echo ""
git log --oneline -3

