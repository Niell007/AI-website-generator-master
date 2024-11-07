import requests
import json
import math
import urllib.request
import os
import base64
import re

def generate_image(style, alt, img_src, local_directory):
    ACCOUNT_ID = os.environ.get('CLOUDFLARE_ACCOUNT_ID', '86e2b8822cebf8584cf942edb3103fae')
    API_KEY = os.environ.get('CLOUDFLARE_API_KEY', 'PwfJor56sIf_CrWSk09eOT3Np9fla4xU8WSrWYrz')
    
    # Extract dimensions from style
    if style is None:
        width_adjusted = 1024
        height_adjusted = 1024
        print("Style not provided, using default dimensions")
    else:
        width_search = re.search('width: (\d+)px', style)
        height_search = re.search('height: (\d+)px', style)
        
        if width_search and height_search:
            width = int(width_search.group(1))
            height = int(height_search.group(1))
            # Adjust dimensions to be compatible with Stable Diffusion
            width_adjusted = min(1024, 64 * math.ceil(width / 64))
            height_adjusted = min(1024, 64 * math.ceil(height / 64))
        else:
            width_adjusted = 1024
            height_adjusted = 1024
            print("No style requirements found, using default dimensions")

    # Cloudflare Workers AI endpoint for Stable Diffusion
    url = f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/ai/run/@cf/stabilityai/stable-diffusion-xl-base-1.0"
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Prepare the prompt for image generation
    prompt = f"{alt} high quality, detailed, professional photograph"
    
    payload = {
        "prompt": prompt,
        "num_steps": 50,
        "width": width_adjusted,
        "height": height_adjusted,
        "negative_prompt": "poorly drawn, bad anatomy, blurry, low quality"
    }

    try:
        print(f"Generating image with prompt: {prompt}")
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        
        result = response.json()
        
        if 'result' in result and 'images' in result['result']:
            # Save the base64 image
            image_data = base64.b64decode(result['result']['images'][0])
            local_image_path = f"{local_directory}/images/{img_src.split('/')[-1].split('.')[0]}.webp"
            
            with open(local_image_path, 'wb') as f:
                f.write(image_data)
                
            print("Image generated:", local_image_path)
            return local_image_path
        else:
            print("Unexpected response format:", result)
            raise Exception("Unexpected response format from Cloudflare AI")
            
    except Exception as e:
        print(f"Error generating image: {str(e)}")
        raise
