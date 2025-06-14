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
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

logging.set_verbosity_error()  # suppresses warnings
warnings.filterwarnings("ignore")
# Load environment variables
load_dotenv()

# Load Pegasus model
pegasus_tokenizer = AutoTokenizer.from_pretrained("tuner007/pegasus_paraphrase")
pegasus_model = AutoModelForSeq2SeqLM.from_pretrained("tuner007/pegasus_paraphrase")

# Your Hugging Face API key
HUGGINGFACE_API_KEY = "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"

# Translation model URL
TRANSLATE_URL = "https://api-inference.huggingface.co/models/Helsinki-NLP/opus-mt-{}-en"
headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}

def translate_to_english(text, source_lang):
    translate_url = TRANSLATE_URL.format(source_lang)
    payload = {"inputs": text}
    response = requests.post(translate_url, headers=headers, json=payload)
    if response.status_code == 200:
        result = response.json()
        return result[0].get('translation_text', None)
    print(f"Error during translation: {response.status_code}")
    return None

def paraphrase_text(text, retries=3):
    try:
        input_text = f"paraphrase: {text}"
        inputs = pegasus_tokenizer(
            [input_text], truncation=True, padding="longest", max_length=128, return_tensors="pt"
        )
        with torch.no_grad():
            outputs = pegasus_model.generate(
                **inputs,
                max_length=150,
                num_return_sequences=1,
                do_sample=True,
                temperature=0.9,
                top_k=50,
                top_p=0.95,
                repetition_penalty=1.2,
                no_repeat_ngram_size=3
            )
        return pegasus_tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
    except Exception as e:
        print(f"Paraphrasing error: {e}")
        return None

def paraphrase_large_text(text, chunk_size=250):
    chunks = textwrap.wrap(text, width=chunk_size)
    paraphrased_chunks = []
    for chunk in chunks:
        print(f"Paraphrasing chunk: {chunk[:50]}...")
        paraphrased = paraphrase_text(chunk)
        paraphrased_chunks.append(paraphrased or chunk)
    return " ".join(paraphrased_chunks)

def pre_process_text(text, lang='en'):
    if lang != 'en':
        print(f"Translating from {lang} to English...")
        translated_text = translate_to_english(text, lang)
        if translated_text:
            text = translated_text
        else:
            return None
    print("Paraphrasing large text...")
    return paraphrase_large_text(text).replace("paraphrasedoutput:", "")

def process_text(text, image_urls):
    abbreviations = ['approx.', 'e.g.', 'i.e.']
    for abbr in abbreviations:
        text = text.replace(abbr, abbr.replace('.', '[DOT]'))
    sentences = re.split(r'(?<!\d)(?<!\S@)\.(?!\d)(?!\S)', text)
    sentences = [s.replace('[DOT]', '.').strip().capitalize() for s in sentences if s.strip()]

    if len(image_urls) == 1:
        text_block = ''.join([f'<p style="font-size: 16px; margin: 0; line-height: 1.6;">{s}.</p><br>' for s in sentences])
        return f'''
        <div style="font-size: 19px; line-height: 1.6;">
            <img src="{image_urls[0]}" alt="Image Illustration" style="width:100%;height:auto; display: block; margin-bottom: 20px;"><br>
            <h1 style="font-size: 40px;font-weight: bold;font-family: Helvetica, sans-serif;">{paraphrased_title}</h1><br>
            {text_block}
        </div>'''

    midpoint = len(sentences) // 2
    first_half = ''.join([f'<p style="font-size: 16px; margin: 0; line-height: 1.6;">{s}.</p><br>' for s in sentences[:midpoint]])
    second_half = ''.join([f'<p style="font-size: 16px; margin: 0; line-height: 1.6;">{s}.</p><br>' for s in sentences[midpoint:]])
    image_tags = ''.join([f'<a href="{url}" style="flex: 1 1 calc(25% - 20px); margin: 10px;"><img src="{url}" alt="Image" style="width: 230px; height: 200px;border-radius: 5px;border: 1px solid #ccc;"></a>' for url in image_urls])
    image_container = f'<div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 10px; margin: 20px 0;">{image_tags}</div>'

    return f'''
    <div style="font-size: 19px; line-height: 1.6;">
        <img src="{image_urls[0]}" alt="Image Illustration" style="width:100%;height:auto; display: block; margin-bottom: 20px;"><br>
        <h1 style="font-size: 40px;font-weight: bold;font-family: Helvetica, sans-serif;">{paraphrased_title}</h1><br>
        {first_half}
        {image_container}
        {second_half}
    </div>'''

def sanitize_slug(slug):
    slug = re.sub(r'[^a-zA-Z0-9-_]', '-', slug).strip('-')
    if not re.match(r'^[a-zA-Z0-9]', slug):
        slug = 'a' + slug
    return slug

def create_new_article():
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
            "main-image": {"url": img_url, "alt": "Image Illustration"},
            "tags": ["6553e71600ad68934cb80cd6"],
            "order": 0
        },
        "isDraft": False
    }

def add_article_to_webflow(article):
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {os.getenv('WEBFLOW_API_KEY')}"
    }
    url = f"https://api.webflow.com/v2/collections/{os.getenv('COLLECTION_ID')}/items"
    response = requests.post(url, json=article, headers=headers)
    if response.status_code in [200, 201]:
        print("Article added successfully!")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"Failed to add article. Status code: {response.status_code}")
        print(response.text)

# Main execution loop
results = parse_urls()
for result in results:
    print('processing....')
    text, img_url, title = result
    images = img_url[1:] if len(img_url) > 1 else [img_url[0]]
    img_url = img_url[0]
    detected_language = detect(text)
    print(f"Detected language: {detected_language}")
    paraphrased_title = paraphrase_text(title).replace("paraphrasedoutput:", "")
    paraphrased_output = pre_process_text(text, detected_language)
    formatted_html = process_text(paraphrased_output, images)
    valid_slug = sanitize_slug(paraphrased_title)
    print('Uploading to Webflow Next Url Data...')
    new_article = create_new_article()
    add_article_to_webflow(new_article)
    time.sleep(5)
print('Process Completed')
