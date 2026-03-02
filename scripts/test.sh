#!/bin/bash
# ESP32 Python Keyboard - Test Runner Script

set -e

echo "=== Running Tests ==="

# Activate virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Check if tests directory exists
if [ ! -d "tests" ]; then
    echo "Error: tests/ directory not found"
    exit 1
fi

# Run pytest with coverage
echo "Running pytest..."
pytest tests/ -v --cov=src --cov-report=term-missing

# Show coverage summary
echo ""
echo "=== Test Complete ==="
