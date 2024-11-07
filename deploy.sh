#!/bin/bash

# Make script exit on error
set -e

# Print with colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}🚀 AI Website Generator Deployment Script${NC}"

# Check Python installation
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python not found. Please install Python 3.9+${NC}"
    exit 1
fi

# Check Git installation
if ! command -v git &> /dev/null; then
    echo -e "${RED}❌ Git not found. Please install Git${NC}"
    exit 1
fi

# Create virtual environment
echo -e "${YELLOW}📦 Creating virtual environment...${NC}"
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo -e "${YELLOW}📥 Installing dependencies...${NC}"
pip install -r requirements.txt

# Setup environment file
if [ ! -f .env ]; then
    echo -e "${YELLOW}⚙️ Setting up environment file...${NC}"
    cp .env.example .env
    
    # Get user input for environment variables
    read -p "Enter your Cloudflare API Key: " cloudflareApiKey
    read -p "Enter your Cloudflare Account ID: " cloudflareAccountId
    read -p "Enter your GitHub Access Token: " githubToken
    read -p "Enter your GitHub Repository Name: " githubRepo
    read -p "Enter your Git Email: " gitEmail
    read -p "Enter your Git Username: " gitName
    
    # Update .env file
    sed -i "s/CLOUDFLARE_API_KEY=.*/CLOUDFLARE_API_KEY=$cloudflareApiKey/" .env
    sed -i "s/CLOUDFLARE_ACCOUNT_ID=.*/CLOUDFLARE_ACCOUNT_ID=$cloudflareAccountId/" .env
    sed -i "s/GITHUB_ACCESS_TOKEN=.*/GITHUB_ACCESS_TOKEN=$githubToken/" .env
    sed -i "s/GITHUB_REPO_NAME=.*/GITHUB_REPO_NAME=$githubRepo/" .env
    sed -i "s/GIT_USER_EMAIL=.*/GIT_USER_EMAIL=$gitEmail/" .env
    sed -i "s/GIT_USER_NAME=.*/GIT_USER_NAME=$gitName/" .env
fi

# Create images directory if it doesn't exist
mkdir -p images

# Make deploy.sh executable
chmod +x deploy.sh

# Start the application
echo -e "${GREEN}🌟 Starting the application...${NC}"
flask run 