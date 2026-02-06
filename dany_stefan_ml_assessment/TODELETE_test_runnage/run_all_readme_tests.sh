#!/bin/bash
# Master script to run all README reproducibility tests

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "=========================================="
echo "README REPRODUCIBILITY TEST SUITE"
echo "=========================================="
echo "Testing if another person can follow the README"
echo ""
echo "Project: $PROJECT_ROOT"
echo "Test Suite: $SCRIPT_DIR"
echo ""
echo "=========================================="
echo ""

# Determine Python executable
if [ -f "$PROJECT_ROOT/../.venv/bin/python" ]; then
    PYTHON="$PROJECT_ROOT/../.venv/bin/python"
elif command -v python3 &> /dev/null; then
    PYTHON="python3"
elif command -v python &> /dev/null; then
    PYTHON="python"
else
    echo "❌ ERROR: No Python found"
    exit 1
fi

echo "Using Python: $PYTHON"
$PYTHON --version
echo ""
echo "=========================================="

# Test 1: Setup Instructions
echo ""
echo "🧪 TEST SUITE 1: README Setup Instructions"
echo "=========================================="
$PYTHON "$SCRIPT_DIR/test_readme_setup_instructions.py"
TEST1=$?
echo ""

# Test 2: Command Reproducibility
echo ""
echo "🧪 TEST SUITE 2: README Command Reproducibility"
echo "=========================================="
$PYTHON "$SCRIPT_DIR/test_readme_commands.py"
TEST2=$?
echo ""

# Test 3: Workflow Simulation
echo ""
echo "🧪 TEST SUITE 3: End-to-End Workflow Simulation"
echo "=========================================="
$PYTHON "$SCRIPT_DIR/test_readme_workflow.py"
TEST3=$?
echo ""

# Test 4: Reproducibility (skip LightGBM)
if [ -f "$SCRIPT_DIR/test_reproducibility.py" ]; then
    echo ""
    echo "🧪 TEST SUITE 4: Core Reproducibility (Skip LightGBM)"
    echo "=========================================="
    $PYTHON "$SCRIPT_DIR/test_reproducibility.py"
    TEST4=$?
    echo ""
else
    TEST4=0
fi

# Final Summary
echo ""
echo "=========================================="
echo "FINAL TEST RESULTS"
echo "=========================================="
echo ""

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

if [ $TEST1 -eq 0 ]; then
    echo -e "${GREEN}✓ PASS${NC} - Setup Instructions"
else
    echo -e "${RED}✗ FAIL${NC} - Setup Instructions"
fi

if [ $TEST2 -eq 0 ]; then
    echo -e "${GREEN}✓ PASS${NC} - Command Reproducibility"
else
    echo -e "${RED}✗ FAIL${NC} - Command Reproducibility"
fi

if [ $TEST3 -eq 0 ]; then
    echo -e "${GREEN}✓ PASS${NC} - Workflow Simulation"
else
    echo -e "${RED}✗ FAIL${NC} - Workflow Simulation"
fi

if [ $TEST4 -eq 0 ]; then
    echo -e "${GREEN}✓ PASS${NC} - Core Reproducibility"
else
    echo -e "${RED}✗ FAIL${NC} - Core Reproducibility"
fi

echo ""
echo "=========================================="

# Calculate pass rate
TOTAL=0
PASSED=0

if [ $TEST1 -eq 0 ]; then ((PASSED++)); fi
if [ $TEST2 -eq 0 ]; then ((PASSED++)); fi
if [ $TEST3 -eq 0 ]; then ((PASSED++)); fi
if [ $TEST4 -eq 0 ]; then ((PASSED++)); fi

TOTAL=4

PASS_RATE=$((PASSED * 100 / TOTAL))

echo "Pass Rate: $PASSED/$TOTAL ($PASS_RATE%)"
echo ""

if [ $PASSED -eq $TOTAL ]; then
    echo -e "${GREEN}✅ ALL TESTS PASSED${NC}"
    echo "README is fully reproducible!"
    exit 0
elif [ $PASS_RATE -ge 75 ]; then
    echo -e "${YELLOW}⚠️ MOSTLY REPRODUCIBLE${NC}"
    echo "README works but has some issues."
    exit 1
else
    echo -e "${RED}❌ REPRODUCIBILITY ISSUES${NC}"
    echo "README needs improvements for others to follow."
    exit 1
fi
