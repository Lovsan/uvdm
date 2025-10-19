#!/bin/bash
# Startup script for UVDM with API server

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  UVDM Startup Script${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# Check if virtual environment should be used
if [ -d "venv" ]; then
    echo -e "${YELLOW}Activating virtual environment...${NC}"
    source venv/bin/activate
fi

# Load configuration if exists
if [ -f "api_config.env" ]; then
    echo -e "${YELLOW}Loading API configuration...${NC}"
    export $(grep -v '^#' api_config.env | xargs)
fi

# Check if we should start the API server
if [ "$1" == "--with-api-server" ] || [ "$1" == "-a" ]; then
    echo -e "${YELLOW}Starting API server in background...${NC}"
    python api_server.py > api_server.log 2>&1 &
    API_PID=$!
    echo -e "${GREEN}API server started (PID: $API_PID)${NC}"
    echo $API_PID > api_server.pid
    
    # Wait a moment for server to start
    sleep 2
    
    # Check if server is running
    if curl -s http://localhost:${UVDM_API_PORT:-5000}/ > /dev/null 2>&1; then
        echo -e "${GREEN}API server is running at http://localhost:${UVDM_API_PORT:-5000}${NC}"
    else
        echo -e "${RED}Warning: API server may not be running correctly${NC}"
    fi
    echo ""
fi

# Start the main application
echo -e "${YELLOW}Starting UVDM application...${NC}"
python main.py

# Cleanup
if [ -f "api_server.pid" ]; then
    API_PID=$(cat api_server.pid)
    echo ""
    echo -e "${YELLOW}Stopping API server (PID: $API_PID)...${NC}"
    kill $API_PID 2>/dev/null
    rm api_server.pid
    echo -e "${GREEN}API server stopped${NC}"
fi

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  UVDM Shutdown Complete${NC}"
echo -e "${GREEN}========================================${NC}"
