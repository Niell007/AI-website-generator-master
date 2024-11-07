import requests
import os
import json

def generate_html(prompt):
    ACCOUNT_ID = os.environ.get('CLOUDFLARE_ACCOUNT_ID', '86e2b8822cebf8584cf942edb3103fae')
    API_KEY = os.environ.get('CLOUDFLARE_API_KEY', 'PwfJor56sIf_CrWSk09eOT3Np9fla4xU8WSrWYrz')
    MODEL = os.environ.get('CLOUDFLARE_AI_MODEL', '@cf/meta/llama-2-7b-chat-int8')
    
    url = f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/ai/run/{MODEL}"
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Format the conversation for Llama-2 style chat
    system_prompt = "You are a professional web developer who creates high-quality HTML code. Always include proper HTML structure, responsive design, and semantic elements."
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt}
    ]
    
    payload = {
        "messages": messages,
        "stream": False,
        "max_tokens": 4096
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        
        result = response.json()
        
        # Check if the response contains the expected structure
        if 'result' in result and 'response' in result['result']:
            content = result['result']['response']
            
            # Extract HTML content if the response contains markdown or other formatting
            if '```html' in content:
                html_content = content.split('```html')[1].split('```')[0].strip()
            else:
                html_content = content.strip()
                
            print("Generated HTML content successfully")
            return html_content
        else:
            print("Unexpected response format:", result)
            raise Exception("Unexpected response format from Cloudflare Workers AI")
            
    except requests.exceptions.RequestException as e:
        print(f"Error calling Cloudflare Workers AI: {str(e)}")
        print(f"Response content: {response.text if 'response' in locals() else 'No response'}")
        raise Exception(f"Failed to generate HTML: {str(e)}")



