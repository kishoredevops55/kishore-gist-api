#!/bin/bash
###############################################################################
# COMPREHENSIVE DEMO SCRIPT - Run all demos to show interviewers
# Safe to run - no production data affected
###############################################################################

set -e  # Exit on error

echo ""
echo "╔════════════════════════════════════════════════════════════════════════╗"
echo "║                                                                        ║"
echo "║           GITHUB GISTS API - COMPREHENSIVE DEMO RUNNER               ║"
echo "║                                                                        ║"
echo "║  This script runs all demos to showcase:                             ║"
echo "║    • Cache functionality and performance                             ║"
echo "║    • GitHub API integration                                          ║"
echo "║    • Load balancing and traffic handling                             ║"
echo "║                                                                        ║"
echo "╚════════════════════════════════════════════════════════════════════════╝"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if API is running
echo -e "${BLUE}Checking if API is running on http://localhost:8080...${NC}"
if ! curl -s http://localhost:8080/health > /dev/null 2>&1; then
    echo -e "${RED}❌ API is not running!${NC}"
    echo ""
    echo "Start the API with:"
    echo "  uvicorn app.main:app --host 0.0.0.0 --port 8080"
    exit 1
fi
echo -e "${GREEN}✅ API is running${NC}"
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is required but not installed${NC}"
    exit 1
fi

echo -e "${YELLOW}Running all demos...${NC}"
echo ""

# Demo 1: Cache Testing
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}DEMO 1: CACHE TESTING${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
python3 demo_cache_testing.py

# Demo 2: GitHub Integration
echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}DEMO 2: GITHUB INTEGRATION${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
python3 demo_github_integration.py

# Demo 3: Load Balancing
echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}DEMO 3: LOAD BALANCING & TRAFFIC${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
python3 demo_load_balancing.py

# Summary
echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✅ ALL DEMOS COMPLETED SUCCESSFULLY!${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo "Summary for Interviewers:"
echo ""
echo "✅ Cache System:"
echo "   • Demonstrates cache hit/miss behavior"
echo "   • Shows performance improvements (10x+ faster)"
echo "   • Automatic TTL management"
echo ""
echo "✅ GitHub Integration:"
echo "   • Real API calls to GitHub"
echo "   • Proper error handling"
echo "   • Rate limit awareness"
echo "   • Token security best practices"
echo ""
echo "✅ Load Balancing:"
echo "   • Handles concurrent requests"
echo "   • Sustained load testing"
echo "   • Multiple user distribution"
echo "   • Kubernetes/Istio setup explanation"
echo ""
echo "🔗 API Endpoints:"
echo "   • GET  /           - Root endpoint"
echo "   • GET  /health     - Health check"
echo "   • GET  /{username} - Get gists"
echo "   • GET  /metrics    - Prometheus metrics"
echo ""
echo "📊 Monitoring:"
echo "   • Prometheus metrics available at: http://localhost:8080/metrics"
echo "   • Grafana dashboards: http://localhost:3000"
echo "   • Check helm/values.yaml for full stack configuration"
echo ""
