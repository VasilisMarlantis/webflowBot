import requests
import time
from langdetect import detect
from scraper import parse
from script import parse_urls
import textwrap
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
PARAPHRASE_URL = "https://api-inference.huggingface.co/models/humarin/chatgpt_paraphraser_on_T5_base"

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
            "max_length": 150  # Control the length of the generated text
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
            # Only append the paraphrased chunk directly
            paraphrased_chunks.append(paraphrased_chunk)
        else:
            paraphrased_chunks.append(chunk)  # In case paraphrasing fails, return the original chunk

    # Join the paraphrased chunks back together without any extra words or prefixes
    return " ".join(paraphrased_chunks)

def pre_process_text(text, lang='en'):
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

    # Remove any occurrence of "paraphrased_output" from the paraphrased text
    clean_text = paraphrased_text.replace("paraphrasedoutput:", "")

    return clean_text


def process_text(text, image_urls):
    # Define a list of common abbreviations
    abbreviations = ['approx.', 'e.g.', 'i.e.']

    # Replace periods in abbreviations with placeholders to avoid splitting them
    for abbr in abbreviations:
        text = text.replace(abbr, abbr.replace('.', '[DOT]'))

    # Split the text into sentences based on the full stop that is not part of a number, a URL, or an email address
    sentences = re.split(r'(?<!\d)(?<!\S@)\.(?!\d)(?!\S)', text)

    # Restore abbreviations by replacing placeholders back to periods
    sentences = [sentence.replace('[DOT]', '.') for sentence in sentences]

    # Strip leading/trailing whitespaces and capitalize the first letter of each sentence
    sentences = [sentence.strip().capitalize() for sentence in sentences if sentence]

    # Check the number of images
    if len(image_urls) == 1:
        # If only one image, do not split the text
        text_block = ''.join([f'<p style="font-size: 16px; margin: 0; line-height: 1.6;">{sentence}.</p><br>' for sentence in sentences])
        
        # HTML content with a single image at the top and the full text below
        html_content = f'''
        <div style="font-size: 19px; line-height: 1.6;">
            <img src="{image_urls[0]}" alt="Image Illustration" style="width:100%;height:auto; display: block; margin-bottom: 20px;"><br>
            <h1 style="font-size: 40px;font-weight: bold;font-family: Helvetica, sans-serif;">{paraphrased_title}</h1><br>
            {text_block}
        </div>
        '''
    else:
        # Split the sentences into two halves if there are multiple images
        midpoint = len(sentences) // 2
        first_half_sentences = sentences[:midpoint]
        second_half_sentences = sentences[midpoint:]

        # Format the sentences into HTML <p> tags
        first_half = ''.join([f'<p style="font-size: 16px; margin: 0; line-height: 1.6;">{sentence}.</p><br>' for sentence in first_half_sentences])
        second_half = ''.join([f'<p style="font-size: 16px; margin: 0; line-height: 1.6;">{sentence}.</p><br>' for sentence in second_half_sentences])

        # Create inline image tags with flexbox for alignment
        image_tags = ''.join([f'<a href="{img_url}" style="flex: 1 1 calc(25% - 20px); margin: 10px;"><img src="{img_url}" alt="Image" style="width: 230px; height: 200px;border-radius: 5px;border: 1px solid #ccc;"></a>' for img_url in image_urls])
         # Wrap images in a flexbox container to display them in a row
        image_container = f'''
        <div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 10px; margin: 20px 0;">
            {image_tags}
        </div>
        '''
        # HTML content with images between the two halves of the text
        html_content = f'''
        <div style="font-size: 19px; line-height: 1.6;">
            <img src="{image_urls[0]}" alt="Image Illustration" style="width:100%;height:auto; display: block; margin-bottom: 20px;"><br>
            <h1 style="font-size: 40px;font-weight: bold;font-family: Helvetica, sans-serif;">{paraphrased_title}</h1><br>
            {first_half}
            <div style="display: flex; justify-content: space-between;align-items: center; gap: 10px; margin: 20px 0;">
                {image_container}
            </div>
            {second_half}
        </div>
        '''

    return html_content


# Webflow API details
WEBFLOW_API_KEY = os.getenv("WEBFLOW_API_KEY")
SITE_ID = os.getenv("SITE_ID") 
COLLECTION_ID = os.getenv("COLLECTION_ID")
WEBFLOW_API_URL = f"https://api.webflow.com/v2/collections/{COLLECTION_ID}/items"


# Parsing slug from title

def sanitize_slug(slug):
    # Ensure slug is a string and not None
    if not isinstance(slug, str) or slug.strip() == "":
        return "default-slug"
    
    # Replace invalid characters with hyphens
    sanitized_slug = re.sub(r'[^a-zA-Z0-9-_]', '-', slug).strip('-')
    
    # Ensure the slug starts with a valid character (letter or number)
    if not re.match(r'^[a-zA-Z0-9]', sanitized_slug):
        sanitized_slug = 'a' + sanitized_slug  # Prefix with 'a' if invalid start

    return sanitized_slug



def create_new_article():
    # Create items for the new article
    new_article = {
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
            "tags": ["6553e71600ad68934cb80cd6"] ,
            "order":0,
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


results = parse_urls()
for result in results:
    print('processing....')
    text, img_url, title = result
    images = img_url[1:] if len(img_url) > 1 else [img_url[0]]
    img_url = img_url[0]
    detected_language = detect(text)
    print(f"Detected language: {detected_language}")
    paraphrased_title = paraphrase_text(title)
    paraphrased_title = paraphrased_title.replace("paraphrasedoutput:", "") if paraphrased_title and "paraphrasedoutput:" in paraphrased_title else paraphrased_title
    paraphrased_output = pre_process_text(text, detected_language)
    formatted_html = process_text(paraphrased_output, images)
    valid_slug = sanitize_slug(paraphrased_title)
    print('Uploading to Webflow Next Url Data...')
    new_article = create_new_article()
    add_article_to_webflow(new_article)
    time.sleep(5)
print('Process Completed')
