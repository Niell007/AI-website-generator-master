# AI Website Generator with Cloudflare Workers AI

## Overview

This application generates custom websites using Cloudflare Workers AI for both text and image generation. It automatically deploys the generated sites to GitHub and Vercel.

## Features

- 🎨 Website generation using Cloudflare AI
- 🖼️ Image generation using Cloudflare Stable Diffusion XL
- 🚀 Automatic GitHub deployment
- ⚡ Vercel integration
- 🐳 Docker support

## Prerequisites

- Python 3.9+
- Git
- Docker (optional)
- Cloudflare account
- GitHub account
- Vercel account

## Quick Start

### Windows (PowerShell)

```powershell
.\deploy.ps1
```

### Linux/MacOS (Bash)

```bash
./deploy.sh
```

## Manual Setup

1. Clone the repository:

```bash
git clone https://github.com/yourusername/AI-website-generator
cd AI-website-generator
```

2. Set up Cloudflare:
   - Create a Cloudflare account
   - Get your Account ID from the dashboard
   - Create an API token with AI permissions
   - Note down: CLOUDFLARE_ACCOUNT_ID and CLOUDFLARE_API_KEY

3. Configure environment:

```bash
cp .env.example .env
```

Edit .env with your credentials:

```env
CLOUDFLARE_API_KEY=your_api_key
CLOUDFLARE_ACCOUNT_ID=your_account_id
CLOUDFLARE_AI_MODEL=@cf/meta/llama-2-7b-chat-int8
GITHUB_ACCESS_TOKEN=your_github_token
GITHUB_REPO_NAME=your_repo_name
GIT_USER_EMAIL=your_email
GIT_USER_NAME=your_name
```

4. Install dependencies:

```bash
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
```

## Deployment Options

### Local Development

```bash
flask run
```

### Docker Deployment

```bash
docker-compose up --build
```

### Render Deployment

1. Connect your GitHub repository to Render
2. Use these settings:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app --timeout 180`
   - Add environment variables from .env

### Vercel Deployment

1. Install Vercel CLI:

```bash
npm i -g vercel
```

2. Deploy:

```bash
vercel
```

## API Endpoints

- `GET /`: Main interface
- `POST /generate`: Generate website
  - Parameters:
    - `input_text`: Website description

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| CLOUDFLARE_API_KEY | Cloudflare API key | Yes |
| CLOUDFLARE_ACCOUNT_ID | Cloudflare account ID | Yes |
| CLOUDFLARE_AI_MODEL | AI model name | Yes |
| GITHUB_ACCESS_TOKEN | GitHub personal access token | Yes |
| GITHUB_REPO_NAME | Target repository name | Yes |
| GIT_USER_EMAIL | Git commit email | Yes |
| GIT_USER_NAME | Git commit name | Yes |

## Directory Structure

```
.
├── app.py              # Flask application
├── beautifulsoup.py    # HTML processing
├── github_utils.py     # GitHub integration
├── main.py            # Core logic
├── openai_utils.py    # Cloudflare AI integration
├── stablehorde.py     # Image generation
├── templates/         # HTML templates
├── workers/          # Cloudflare Workers
├── Dockerfile        # Docker configuration
└── docker-compose.yml # Docker Compose config
```

## Troubleshooting

1. Image Generation Issues:
   - Check Cloudflare API permissions
   - Verify account has AI access enabled

2. Deployment Issues:
   - Verify environment variables
   - Check API key permissions
   - Ensure GitHub token has correct scopes

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License
