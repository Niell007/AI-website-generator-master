# Windows PowerShell Deployment Script
Write-Host "🚀 AI Website Generator Deployment Script" -ForegroundColor Cyan

# Check Python installation
if (!(Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Python not found. Please install Python 3.9+" -ForegroundColor Red
    exit 1
}

# Check Git installation
if (!(Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Git not found. Please install Git" -ForegroundColor Red
    exit 1
}

# Create virtual environment
Write-Host "📦 Creating virtual environment..." -ForegroundColor Yellow
python -m venv venv
.\venv\Scripts\Activate

# Install dependencies
Write-Host "📥 Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

# Setup environment file
if (!(Test-Path .env)) {
    Write-Host "⚙️ Setting up environment file..." -ForegroundColor Yellow
    Copy-Item .env.example .env
    
    $envFile = Get-Content .env
    
    # Get user input for environment variables
    $cloudflareApiKey = Read-Host "Enter your Cloudflare API Key"
    $cloudflareAccountId = Read-Host "Enter your Cloudflare Account ID"
    $githubToken = Read-Host "Enter your GitHub Access Token"
    $githubRepo = Read-Host "Enter your GitHub Repository Name"
    $gitEmail = Read-Host "Enter your Git Email"
    $gitName = Read-Host "Enter your Git Username"
    
    # Update .env file
    $envFile = $envFile -replace "CLOUDFLARE_API_KEY=.*", "CLOUDFLARE_API_KEY=$cloudflareApiKey"
    $envFile = $envFile -replace "CLOUDFLARE_ACCOUNT_ID=.*", "CLOUDFLARE_ACCOUNT_ID=$cloudflareAccountId"
    $envFile = $envFile -replace "GITHUB_ACCESS_TOKEN=.*", "GITHUB_ACCESS_TOKEN=$githubToken"
    $envFile = $envFile -replace "GITHUB_REPO_NAME=.*", "GITHUB_REPO_NAME=$githubRepo"
    $envFile = $envFile -replace "GIT_USER_EMAIL=.*", "GIT_USER_EMAIL=$gitEmail"
    $envFile = $envFile -replace "GIT_USER_NAME=.*", "GIT_USER_NAME=$gitName"
    
    Set-Content .env $envFile
}

# Create images directory if it doesn't exist
if (!(Test-Path images)) {
    New-Item -ItemType Directory -Path images
}

# Start the application
Write-Host "🌟 Starting the application..." -ForegroundColor Green
flask run 