import requests
import time
from langdetect import detect
from scraper import parse
import textwrap
import requests
import json
from datetime import datetime, timedelta
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
            return None
    else:
        print(f"Error during translation: {response.status_code}")
        return None

def paraphrase_text(text, retries=3):
    # Payload to be sent to the paraphrasing API
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
                    paraphrased = result[0]['generated_text']
                    return paraphrased.strip()
                else:
                    return "No 'generated_text' found in response."
            else:
                print(f"Error: {response.status_code}")
        except Exception as e:
            print(f"Error during paraphrasing: {e}")

        print("Retrying...")
        time.sleep(2)

    return None

def paraphrase_large_text(text, chunk_size=250):
    # Split the text into chunks of size <= chunk_size characters
    chunks = textwrap.wrap(text, width=chunk_size)
    
    paraphrased_chunks = []
    
    for chunk in chunks:
        print(f"Paraphrasing chunk: {chunk[:50]}...")  # Show the first 50 characters of each chunk
        paraphrased_chunk = paraphrase_text(chunk)
        if paraphrased_chunk:
            paraphrased_chunks.append(paraphrased_chunk)
        else:
            paraphrased_chunks.append(chunk)  # In case paraphrasing fails, return original chunk

    # Join the paraphrased chunks back together
    return " ".join(paraphrased_chunks)

def process_text(text, lang='en'):
    if lang != 'en':  # If the language is not English, translate it
        print(f"Translating from {lang} to English...")
        translated_text = translate_to_english(text, lang)
        if translated_text:
            print(f"Translated Text: {translated_text}")
            text = translated_text
        else:
            print("Translation failed.")
            return None

    print("Paraphrasing large text...")
    paraphrased_text = paraphrase_large_text(text)
    
    return paraphrased_text

# Example usage
text, img_url, title = parse()  # Get text from your scraper

detected_language = detect(text)
print(f"Detected language: {detected_language}")
paraphrased_title = paraphrase_text(title)
print(f"Paraphrased title: {paraphrased_title}")
paraphrased_output = process_text(text, detected_language)

print("---------------Original Text:", text)
print("===============Paraphrased Text:", paraphrased_output)


# Webflow API details
WEBFLOW_API_KEY = os.getenv("WEBFLOW_API_KEY")
SITE_ID = os.getenv("SITE_ID") 
COLLECTION_ID = os.getenv("COLLECTION_ID")
WEBFLOW_API_URL = f"https://api.webflow.com/v2/collections/{COLLECTION_ID}/items"

#adding new line to text full stop 
def add_new_lines(text):
    # Split the text into sentences based on the full stop
    sentences = text.split('.')
    
    # Create a new list to hold the modified sentences
    modified_text = []
    
    # Iterate over the sentences and group them
    for i in range(len(sentences)):
        # Strip leading/trailing whitespace and check for non-empty sentences
        sentence = sentences[i].strip()
        if sentence:
            modified_text.append(sentence)
        
        # Add a new line after every two sentences
        if (i + 1) % 2 == 0 and i + 1 != len(sentences):
            modified_text.append('\n')  # Append a new line

    # Join the modified sentences into a single string
    return '. '.join(modified_text).strip()

modified_text = add_new_lines(paraphrased_output)


# parsing slug from title
def sanitize_slug(slug):
    # Replace invalid characters with hyphens
    sanitized_slug = re.sub(r'[^a-zA-Z0-9-_]', '-', slug).strip('-')
    
    # Ensure the slug starts with a valid character (letter or number)
    if not re.match(r'^[a-zA-Z0-9]', sanitized_slug):
        sanitized_slug = 'a' + sanitized_slug  # Prefix with 'a' if invalid start
    
    return sanitized_slug

valid_slug = sanitize_slug(title[0])
def create_new_article():
    # Create dummy data for the new article
    new_article = {
        "fieldData": {
            "name": title[0],
            "slug": valid_slug,
            "trending": True,
            "link-stat": "https://jimag.webflow.io/?tab=Culture",
            "culture": True,
            "date-publish": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
            "editor-s-picks": False,
            "fashion": False,
            "luxury": False,
            "stat-select": "Fashion",
            "post-body": modified_text,
            "main-image": {
                "url": img_url ,
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
print(' Uploding to Webflow ...')
new_article = create_new_article()
add_article_to_webflow(new_article)
