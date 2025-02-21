import requests
from PIL import Image
from io import BytesIO
from bs4 import BeautifulSoup
from transformers import AutoProcessor, BlipForConditionalGeneration

def generate_captions(url):
    processor = AutoProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
    
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    img_elements = soup.find_all('img')
    captions = {}
    
    for img_element in img_elements:
        img_url = img_element.get('src')
        if not img_url or 'svg' in img_url or '1x1' in img_url:
            continue
        
        if img_url.startswith('//'):
            img_url = 'https:' + img_url
        elif not img_url.startswith('http'):
            continue
        
        try:
            img_response = requests.get(img_url)
            raw_image = Image.open(BytesIO(img_response.content))
            if raw_image.size[0] * raw_image.size[1] < 400:
                continue
            
            raw_image = raw_image.convert('RGB')
            inputs = processor(raw_image, return_tensors="pt")
            out = model.generate(**inputs, max_new_tokens=50)
            caption = processor.decode(out[0], skip_special_tokens=True)
            
            captions[img_url] = caption
        except Exception as e:
            print(f"Error processing image {img_url}: {e}")
            continue
    
    return captions