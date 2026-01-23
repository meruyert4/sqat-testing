#!/bin/bash

# Aviasales Test Automation - Quick Start Script
# This script helps you set up and run the tests quickly

echo "======================================"
echo "Aviasales Automation - Quick Start"
echo "======================================"
echo ""

# Navigate to project directory
cd "$(dirname "$0")"

echo "Step 1: Cleaning previous builds..."
mvn clean

echo ""
echo "Step 2: Installing dependencies..."
mvn install -DskipTests

echo ""
echo "Step 3: Running tests..."
mvn test

echo ""
echo "======================================"
echo "Test Execution Complete!"
echo "======================================"
echo ""
echo "📊 View Reports:"
echo "   • Extent Report: test-output/ExtentReport.html"
echo "   • Logs: test-output/logs/automation.log"
echo "   • Screenshots: test-output/screenshots/"
echo ""
echo "Open Extent Report:"
echo "   open test-output/ExtentReport.html"
echo ""
