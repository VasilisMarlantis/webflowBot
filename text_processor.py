import requests
import time
from langdetect import detect
from scraper import parse
from script import parse_urls
import textwrap
import json
from datetime import datetime
import os
import re
from dotenv import load_dotenv

load_dotenv()

HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
TRANSLATE_URL = "https://api-inference.huggingface.co/models/Helsinki-NLP/opus-mt-{}-en"
PARAPHRASE_URL = "https://api-inference.huggingface.co/models/google-t5/t5-base"

headers = {
    "Authorization": f"Bearer {HUGGINGFACE_API_KEY}"
}

def translate_to_english(text, source_lang):
    translate_url = TRANSLATE_URL.format(source_lang)
    payload = {"inputs": text}
    response = requests.post(translate_url, headers=headers, json=payload)

    if response.status_code == 200:
        result = response.json()
        return result[0].get('translation_text')
    else:
        print(f"Error during translation: {response.status_code}")
        return None

def paraphrase_text(text, retries=3):
    payload = {
        "inputs": text,
        "parameters": {"max_length": 150},
        "options": {"wait_for_model": True}
    }
    for attempt in range(retries):
        try:
            response = requests.post(PARAPHRASE_URL, headers=headers, json=payload)
            if response.status_code == 200:
                result = response.json()
                return result[0].get('generated_text', '').strip()
        except Exception as e:
            print(f"Error during paraphrasing: {e}")
        print("Retrying...")
        time.sleep(2)
    return None

def paraphrase_large_text(text, chunk_size=250):
    chunks = textwrap.wrap(text, width=chunk_size)
    paraphrased_chunks = []
    for chunk in chunks:
        print(f"Paraphrasing chunk: {chunk[:50]}...")
        paraphrased_chunk = paraphrase_text(chunk)
        paraphrased_chunks.append(paraphrased_chunk or chunk)
    return " ".join(paraphrased_chunks).replace("paraphrasedoutput:", "")

def pre_process_text(text, lang='en'):
    if lang != 'en':
        print(f"Translating from {lang} to English...")
        translated_text = translate_to_english(text, lang)
        if translated_text:
            text = translated_text
        else:
            print("Translation failed.")
            return None
    print("Paraphrasing large text...")
    return paraphrase_large_text(text)

def sanitize_slug(slug):
    if not isinstance(slug, str) or not slug.strip():
        return "default-slug"
    sanitized = re.sub(r'[^a-zA-Z0-9-_]', '-', slug).strip('-')
    if not re.match(r'^[a-zA-Z0-9]', sanitized):
        sanitized = 'a' + sanitized
    return sanitized.lower()

def process_text(text, image_urls, paraphrased_title):
    abbreviations = ['approx.', 'e.g.', 'i.e.']
    for abbr in abbreviations:
        text = text.replace(abbr, abbr.replace('.', '[DOT]'))
    sentences = re.split(r'(?<!\d)(?<!\S@)\.(?!\d)(?!\S)', text)
    sentences = [s.replace('[DOT]', '.').strip().capitalize() for s in sentences if s]

    if len(image_urls) == 1:
        text_block = ''.join([f'<p style="font-size: 16px; margin: 0; line-height: 1.6;">{s}.</p><br>' for s in sentences])
        return f'''
        <div style="font-size: 19px; line-height: 1.6;">
            <img src="{image_urls[0]}" alt="Image Illustration" style="width:100%;height:auto; display: block; margin-bottom: 20px;"><br>
            <h1 style="font-size: 40px;font-weight: bold;font-family: Helvetica, sans-serif;">{paraphrased_title}</h1><br>
            {text_block}
        </div>
        '''
    else:
        midpoint = len(sentences) // 2
        first_half = ''.join([f'<p style="font-size: 16px; margin: 0; line-height: 1.6;">{s}.</p><br>' for s in sentences[:midpoint]])
        second_half = ''.join([f'<p style="font-size: 16px; margin: 0; line-height: 1.6;">{s}.</p><br>' for s in sentences[midpoint:]])
        image_tags = ''.join([f'<a href="{url}" style="flex: 1 1 calc(25% - 20px); margin: 10px;"><img src="{url}" style="width: 230px; height: 200px;border-radius: 5px;border: 1px solid #ccc;"></a>' for url in image_urls])
        image_container = f'<div style="display: flex; flex-wrap: wrap; justify-content: space-between; gap: 10px; margin: 20px 0;">{image_tags}</div>'
        return f'''
        <div style="font-size: 19px; line-height: 1.6;">
            <img src="{image_urls[0]}" alt="Image Illustration" style="width:100%;height:auto; display: block; margin-bottom: 20px;"><br>
            <h1 style="font-size: 40px;font-weight: bold;font-family: Helvetica, sans-serif;">{paraphrased_title}</h1><br>
            {first_half}
            {image_container}
            {second_half}
        </div>
        '''

WEBFLOW_API_KEY = os.getenv("WEBFLOW_API_KEY")
SITE_ID = os.getenv("SITE_ID")
COLLECTION_ID = os.getenv("COLLECTION_ID")
WEBFLOW_API_URL = f"https://api.webflow.com/v2/collections/{COLLECTION_ID}/items"

def create_new_article(paraphrased_title, valid_slug, formatted_html, img_url):
    return {
        "fieldData": {
            "name": paraphrased_title,
            "slug": valid_slug,
            "trending": True,
            "link-stat": "https://jimag.webflow.io/?tab=Culture",
            "culture": False,
            "date-publish": datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "editor-s-picks": False,
            "fashion": False,
            "luxury": False,
            "stat-select": "Culture",
            "post-body": formatted_html,
            "main-image": {
                "url": img_url,
                "alt": "Image Illustration"
            },
            "tags": ["6553e71600ad68934cb80cd6"],
            "order": 0
        },
        "isDraft": False
    }

def add_article_to_webflow(article):
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {WEBFLOW_API_KEY}"
    }
    response = requests.post(WEBFLOW_API_URL, json=article, headers=headers)
    if response.status_code in [200, 201]:
        print("✅ Article added successfully!")
    else:
        print(f"❌ Failed to add article. Status: {response.status_code}")
        print(response.text)

# ------------- MAIN LOGIC -------------
results = parse_urls()
for result in results:
    print('Processing...')
    text, img_urls, title = result
    if not text or not img_urls:
        continue

    img_url = img_urls[0]
    images = img_urls[1:] if len(img_urls) > 1 else [img_url]

    detected_language = detect(text)
    paraphrased_title = paraphrase_text(title)
    if not paraphrased_title:
        print("Title paraphrasing failed, skipping...")
        continue

    valid_slug = sanitize_slug(paraphrased_title)

    processed_text = pre_process_text(text, lang=detected_language)
    if not processed_text:
        print("Text processing failed, skipping...")
        continue

    formatted_html = process_text(processed_text, images, paraphrased_title)

    article_data = create_new_article(paraphrased_title, valid_slug, formatted_html, img_url)
    add_article_to_webflow(article_data)
