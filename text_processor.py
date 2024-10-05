import requests
import time
from langdetect import detect
from scraper import parse
import textwrap
import json
from datetime import datetime
import os
import re
from dotenv import load_dotenv

load_dotenv()

# Your Hugging Face API key
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

# API URLs for translation and paraphrasing
TRANSLATE_URL = "https://api-inference.huggingface.co/models/Helsinki-NLP/opus-mt-{}-en"
PARAPHRASE_URL = "https://api-inference.huggingface.co/models/ramsrigouthamg/t5-large-paraphraser-diverse-high-quality"

# The headers containing the API key
headers = {
    "Authorization": f"Bearer {HUGGINGFACE_API_KEY}"
}

def translate_to_english(text, source_lang):
    # URL for translation from the source language to English
    translate_url = TRANSLATE_URL.format(source_lang)
    
    payload = {
        "inputs": text
    }
    
    response = requests.post(translate_url, headers=headers, json=payload)
    
    if response.status_code == 200:
        result = response.json()
        if 'translation_text' in result[0]:
            return result[0]['translation_text']
    else:
        print(f"Error during translation: {response.status_code}")
    return None

def paraphrase_text(text, retries=3):
    payload = {
        "inputs": text,
        "parameters": {
            "max_length": 250  # Control the length of the generated text
        },
        "options": {"wait_for_model": True}
    }

    for attempt in range(retries):
        try:
            response = requests.post(PARAPHRASE_URL, headers=headers, json=payload)
            if response.status_code == 200:
                result = response.json()
                if 'generated_text' in result[0]:
                    return result[0]['generated_text'].strip()
            else:
                print(f"Error: {response.status_code}")
        except Exception as e:
            print(f"Error during paraphrasing: {e}")

        print("Retrying...")
        time.sleep(2)

    return None

def paraphrase_large_text(text, chunk_size=250):
    chunks = textwrap.wrap(text, width=chunk_size)
    
    paraphrased_chunks = []
    
    for chunk in chunks:
        print(f"Paraphrasing chunk: {chunk[:50]}...")  # Show the first 50 characters of each chunk
        paraphrased_chunk = paraphrase_text(chunk)
        if paraphrased_chunk:
            paraphrased_chunks.append(paraphrased_chunk)
        else:
            paraphrased_chunks.append(chunk)

    return " ".join(paraphrased_chunks)

def process_text(text, lang='en'):
    if lang != 'en':  # If the language is not English, translate it
        print(f"Translating from {lang} to English...")
        translated_text = translate_to_english(text, lang)
        if translated_text:
            text = translated_text
        else:
            print("Translation failed.")
            return None

    print("Paraphrasing large text...")
    paraphrased_text = paraphrase_large_text(text)

    # Remove any occurrence of "paraphrased_output" from the paraphrased text
    clean_text = paraphrased_text.replace("paraphrasedoutput:", "")

    return clean_text

# Example usage
articles = parse()  # Get articles from your scraper

for article in articles:
    # Ensure the article is structured correctly
    if not isinstance(article, dict) or 'text' not in article or 'img_url' not in article or 'title' not in article:
        print("Skipping article due to unexpected structure.")
        continue  # Skip this iteration if the structure is incorrect

    # Unpack the variables
    text = article['text']
    img_url = article['img_url']
    title = article['title']

    # Check if any value is None
    if text is None or img_url is None or title is None:
        print("Skipping article due to missing values.")
        continue

    detected_language = detect(text)
    print(f"Detected language: {detected_language}")
    paraphrased_title = paraphrase_text(title)
    print(f"Paraphrased title: {paraphrased_title}")
    paraphrased_output = process_text(text, detected_language)

    print("=============== Paraphrased Text:", paraphrased_output)

    # Webflow API details
    WEBFLOW_API_KEY = os.getenv("WEBFLOW_API_KEY")
    SITE_ID = os.getenv("SITE_ID") 
    COLLECTION_ID = os.getenv("COLLECTION_ID")
    WEBFLOW_API_URL = f"https://api.webflow.com/v2/collections/{COLLECTION_ID}/items"

    def sanitize_slug(slug):
        sanitized_slug = re.sub(r'[^a-zA-Z0-9-_]', '-', slug).strip('-')
        if not re.match(r'^[a-zA-Z0-9]', sanitized_slug):
            sanitized_slug = 'a' + sanitized_slug
        return sanitized_slug

    valid_slug = sanitize_slug(title)

    def create_new_article():
        new_article = {
            "fieldData": {
                "name": title,
                "slug": valid_slug,
                "trending": True,
                "link-stat": "https://jimag.webflow.io/?tab=Culture",
                "culture": True,
                "date-publish": datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                "editor-s-picks": False,
                "fashion": False,
                "luxury": False,
                "stat-select": "Fashion",
                "post-body": paraphrased_output,
                "main-image": {
                    "url": img_url,
                    "alt": "Image Illustration"
                },
                "tags": ["6553e71600ad68934cb80cd6"] 
            },
            "isDraft": False
        }
        return new_article

    def add_article_to_webflow(article):
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Bearer {WEBFLOW_API_KEY}"
        }

        response = requests.post(WEBFLOW_API_URL, json=article, headers=headers)

        if response.status_code in [200, 201]:
            print("Article added successfully!")
            print(json.dumps(response.json(), indent=2))
        else:
            print(f"Failed to add article. Status code: {response.status_code}")
            print(response.text)

    # Create and add the new article
    print('Uploading to Webflow ...')
    new_article = create_new_article()
    add_article_to_webflow(new_article)
