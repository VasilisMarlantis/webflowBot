# import requests
# import time
# from langdetect import detect, detect_langs
# # Your Hugging Face API key
# API_KEY = "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"

# # API URLs for translation and paraphrasing
# TRANSLATE_URL = "https://api-inference.huggingface.co/models/Helsinki-NLP/opus-mt-{}-en"
# PARAPHRASE_URL = "https://api-inference.huggingface.co/models/ramsrigouthamg/t5-large-paraphraser-diverse-high-quality"

# # The headers containing the API key
# headers = {
#     "Authorization": f"Bearer {API_KEY}"
# }

# def translate_to_english(text, source_lang):
#     # URL for translation from the source language to English
#     translate_url = TRANSLATE_URL.format(source_lang)
    
#     payload = {
#         "inputs": text
#     }
    
#     response = requests.post(translate_url, headers=headers, json=payload)
    
#     if response.status_code == 200:
#         result = response.json()
#         if 'translation_text' in result[0]:
#             return result[0]['translation_text']
#         else:
#             return None
#     else:
#         print(f"Error during translation: {response.status_code}")
#         return None

# def paraphrase_text(text, retries=3):
#     # Payload to be sent to the paraphrasing API
#     payload = {
#         "inputs": text,
#         "parameters": {
#             "max_length": 150  # Control the length of the generated text
#         },
#         "options": {"wait_for_model": True}
#     }

#     for attempt in range(retries):
#         try:
#             response = requests.post(PARAPHRASE_URL, headers=headers, json=payload)
#             if response.status_code == 200:
#                 result = response.json()
#                 if 'generated_text' in result[0]:
#                     paraphrased = result[0]['generated_text']
#                     return paraphrased.strip()
#                 else:
#                     return "No 'generated_text' found in response."
#             else:
#                 print(f"Error: {response.status_code}")
#         except Exception as e:
#             print(f"Error during paraphrasing: {e}")

#         print("Retrying...")
#         time.sleep(2)

#     return None

# def process_text(text, lang='en'):
#     if lang != 'en':  # If the language is not English, translate it
#         print(f"Translating from {lang} to English...")
#         translated_text = translate_to_english(text, lang)
#         if translated_text:
#             print(f"Translated Text: {translated_text}")
#             text = translated_text
#         else:
#             print("Translation failed.")
#             return None

#     print("Paraphrasing...")
#     paraphrased_text = paraphrase_text(text)
    
#     return paraphrased_text

# # Example usage
# input_text = """On 2 September, American tech giant Apple made it to the top of the Hot Search list on Weibo, China’s Twitter-like platform. The topic was “Apple officially responds to iPhone 16 not supporting WeChat” (#苹果官方回应iPhone16不支持微信#) and it has 290 million views at the time of writing.

# """

# detected_language = detected_language = detect(input_text)
# print(f"Detected language: {detected_language}")
# paraphrased_output = process_text(input_text, detected_language)

# print("Original Text:", input_text)
# print("Paraphrased Text:", paraphrased_output)

########################################################################################################""
 
# # The headers containing the API key
# headers = {
#     "Authorization": f"Bearer {API_KEY}"
# }

# def paraphrase_text(text):
#     # Payload to be sent to the API, with increased max_length
#     payload = {
#         "inputs": text,  # No "paraphrase:" prefix to avoid confusion
#         "parameters": {
#             "max_length": 200  # Increase this number if necessary for longer texts
#         },
#         "options": {"wait_for_model": True}
#     }

#     # Send request to Hugging Face API
#     response = requests.post(API_URL, headers=headers, json=payload)

#     # Check if the request was successful
#     if response.status_code == 200:
#         # Get the result
#         result = response.json()
#         print("API Response:", result)  # Debugging line to see the actual response
        
#         # Extract and return the paraphrased text
#         if 'generated_text' in result[0]:
#             paraphrased = result[0]['generated_text']
#             return paraphrased.strip().replace("paraphrasedoutput:", "").strip()  # Clean up any prefix
#         else:
#             return "No 'generated_text' found in response."
#     else:
#         print(f"Error: {response.status_code}")
#         return None

# # Test the paraphrasing function
# text_to_paraphrase = "Artificial intelligence (AI) has become a significant part of modern technology, shaping various industries from healthcare to finance."
# paraphrased_text = paraphrase_text(text_to_paraphrase)

# print("Original Text:", text_to_paraphrase)
# print("Paraphrased Text:", paraphrased_text)

# print("Original Text:", text_to_paraphrase)
# print("Paraphrased Text:", paraphrased_text)

# Example text to reformulate
# text = ("Artificial intelligence (AI) has become a significant part of modern technology, "
#         "shaping various industries from healthcare to finance. By analyzing vast amounts of data, "
#         "AI systems can identify patterns and make predictions, which helps businesses optimize their operations. "
#         "However, as AI continues to grow, concerns around data privacy, job displacement, and ethical use are also rising. "
#         "It's essential for governments and organizations to create frameworks that ensure AI is used responsibly "
#         "and benefits society as a whole.")



# import requests

# import random

# import time


# # List of 30 User-Agents for rotation

# user_agents = [

#     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",

#     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",

#     "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",

#     "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",

#     "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",

#     "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",

#     "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",

#     "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:89.0) Gecko/20100101 Firefox/89.0",

#     "Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",

#     "Mozilla/5.0 (X11; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",

#     "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.1 Safari/605.1.15",

#     "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:89.0) Gecko/20100101 Firefox/89.0",

#     "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",

#     "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15A372 Safari/604.1",

#     "Mozilla/5.0 (iPad; CPU OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15A5341f Safari/604.1",

#     "Mozilla/5.0 (iPhone; CPU iPhone OS 13_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1 Mobile/15E148 Safari/604.1",

#     "Mozilla/5.0 (iPad; CPU OS 13_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1 Mobile/15E148 Safari/604.1",

#     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36",

#     "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.1 Safari/605.1.15",

#     "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko",

#     "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0",

#     "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0",

#     "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Safari/605.1.15",

#     "Mozilla/5.0 (iPhone; CPU iPhone OS 13_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1 Mobile/15E148 Safari/604.1",

#     "Mozilla/5.0 (Linux; Android 10; SM-G973U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.105 Mobile Safari/537.36",

#     "Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Mobile Safari/537.36",

#     "Mozilla/5.0 (iPhone; CPU iPhone OS 14_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",

#     "Mozilla/5.0 (iPad; CPU OS 14_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",

#     "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0",

#     "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15"

# ]
# def jls_extract_def():
    
#     # Define the URL
#     url = "https://daoinsights.com/"
    
#     # Set custom headers
#     headers = {
#         "User-Agent": random.choice(user_agents),  # Rotate user-agent
#         "Accept-Language": "en-US,en;q=0.9",
#         "Referer": "https://www.google.com/",  # Mimic referral from a trusted source
#     }
    
#     # Delay before making a request to avoid bot detection
#     time.sleep(random.uniform(1, 5))  # Delay between 1 to 5 seconds
    
#     # Send the request
#     try:
#         response = requests.get(url, headers=headers)
    
#         # Print status code
#         print(f"Status Code: {response.status_code}")
    
#     except requests.exceptions.RequestException as e:
#         print(f"Request failed: {e}")
#     return e


# e = jls_extract_def()



############ weflow part #########################

# Webflow API details


import requests
import json
from datetime import datetime, timedelta
import os
# Webflow API details

API_KEY = '13ff929739596aa0d9c8e160be497ee4822f93833420ea36d998ce8c1bf2c964'
SITE_ID = '651edd4c0bcc2eb5950e53da'    
COLLECTION_ID = "6553e71600ad68934cb80cb0"





# headers = {
#     "accept": "application/json",
#     "authorization": "Bearer 13ff929739596aa0d9c8e160be497ee4822f93833420ea36d998ce8c1bf2c964"
# }

WEBFLOW_API_URL = f"https://api.webflow.com/v2/collections/{COLLECTION_ID}/items"

def create_new_article():
    # Create dummy data for the new article
    new_article = {
        "fieldData": {
            "name": "Exciting New Trends in Fashion Technology",
            "slug": "exciting-new-trends-in-fashion-technology",
            "trending": True,
            "link-stat": "https://example.com/new-article",
            "culture": True,
            "date-publish": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
            "editor-s-picks": False,
            "fashion": True,
            "luxury": False,
            "stat-select": "4409bb06cc4bd5b997c809b226a80daf",
            "post-body": "<p>Fashion technology is evolving rapidly, bringing new innovations to the industry...</p>",
            "main-image": {
                "url": "https://images.pexels.com/photos/21833104/pexels-photo-21833104/free-photo-of-rhume-froid-neige-hiver.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1" ,
                "alt": "Fashion Technology Illustration"
            },
            "tags": ["6553e71600ad68934cb80ccc","6553e71600ad68934cb80cd6","6553e71600ad68934cb80cce","6553e71600ad68934cb80cef"] 
        },
        "isDraft": False
    }

    return new_article

def add_article_to_webflow(article):
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {API_KEY}"
    }

    response = requests.post(WEBFLOW_API_URL, json=article, headers=headers)

    if response.status_code in [200, 201]:
        print("Article added successfully!")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"Failed to add article. Status code: {response.status_code}")
        print(response.text)

# Create and add the new article
new_article = create_new_article()
add_article_to_webflow(new_article)


# Load API key and site ID from .env file

# API_KEY = "26086cbf7bc3967bb0f8a50e60d275f30b658a8d48a1bc075b0f31f08fbeac17"
# SITE_ID = "651edd4c0bcc2eb5950e53da"
# COLLECTION_ID = "6553e71600ad68934cb80cb0"  # Replace with the actual collection ID
# url = f"https://api.webflow.com/sites/{SITE_ID}/collections"

# # Headers for the API request
# headers = {
#     "Authorization": f"Bearer {API_KEY}",
#     "accept-version": "1.0.0"
# }

# def get_collections():
#     response = requests.get(url, headers=headers)

#     if response.status_code == 200:
#         collections = response.json()
#         # Print all collections and their IDs
#         for collection in collections:
#             print(f"Collection Name: {collection['name']}, Collection ID: {collection['_id']}")
#     else:
#         print(f"Failed to retrieve collections. Status code: {response.status_code}")
#         print(response.text)

# # Call the function to retrieve and display collections
# get_collections()

# # API base URL
# url = f"https://api.webflow.com/collections/{COLLECTION_ID}/items"

# # Headers for the API request
# headers = {
#     "Authorization": f"Bearer {API_KEY}",
#     "Content-Type": "application/json",
#     "accept-version": "1.0.0"
# }

# def create_blog_post(name, slug, post_body, date_publish, main_image_url, editor_pick, trending, fashion, culture, luxury, stat_select, link_stat, tag):
#     # Prepare the data payload
#     data = {
#         "fields": {
#             "name": name,  # Blog post name
#             "slug": slug,  # Blog post slug
#             "post-body": post_body,  # Post content
#             "date-publish": date_publish,  # Date to publish the post
#             "main-image": {
#                 "url": main_image_url  # Main image URL
#             },
#             "editor-pick": editor_pick,  # Toggle for Editor's Pick (boolean)
#             "trending": trending,  # Toggle for Trending (boolean)
#             "fashion": fashion,  # Toggle for Fashion (boolean)
#             "culture": culture,  # Toggle for Culture (boolean)
#             "luxury": luxury,  # Toggle for Luxury (boolean)
#             "stat-select": stat_select,  # Dropdown Stat Select
#             "link-stat": link_stat,  # Link Stat
#             "tag": tag  # Tag field
#         }
#     }

#     # Make the POST request to the Webflow API
#     response = requests.post(url, headers=headers, data=json.dumps(data))

#     if response.status_code == 200:
#         print("Blog post created successfully!")
#     else:
#         print(f"Failed to create blog post. Status code: {response.status_code}")
#         print(response.text)

# # Example usage
# name = "New Blog Post"
# slug = "new-blog-post"
# post_body = "<p>This is the content of the blog post.</p>"
# date_publish = "2023-09-24T00:00:00Z"
# main_image_url = "https://images.pexels.com/photos/21833104/pexels-photo-21833104/free-photo-of-rhume-froid-neige-hiver.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"  # URL of the main image
# editor_pick = True
# trending = False
# fashion = True
# culture = False
# luxury = False
# stat_select = "Fashion"
# link_stat = "https://example.com/stat-link"
# tag = "New Arrival"

# create_blog_post(name, slug, post_body, date_publish, main_image_url, editor_pick, trending, fashion, culture, luxury, stat_select, link_stat, tag)















# # Article data
# article_data = {
#     "fields": {
#         "name": "Buzz Surrounding Huawei’s New Trifold Phone",
#         "slug": "buzz-surrounding-huawei-new-trifold-phone",
#         "post_body": """ While many are still debating whether Apple's press conference and the iPhone 16 releases were underwhelming or simply safe and stable, Huawei’s launch on the same day has undoubtedly been more daring.

# The Chinese tech giant introduced its latest smartphone, the Huawei Mate XT, as the “world’s first trifold phone,” boasting the largest and thinnest mobile device available. It features a 10.2-inch display and is just 3.6 mm thick when fully unfolded. However, its price is steep: the 256GB version costs 19,999 RMB (about $2,809), while the 512GB and 1TB versions are priced at 21,999 RMB ($3,090) and 23,999 RMB ($3,371), respectively. Even before its official release, the Mate XT was listed for over 100,000 RMB on platforms like Goofish and Xianyu, Alibaba’s second-hand marketplace.

# Huawei’s unique “Tiangong” hinge design, combined with the phone’s large size and hefty price tag, has sparked memes comparing it to an imperial throne. The resemblance lies not just in the folding style but also in the phone’s target demographic—business executives who, according to Richard Yu Chengdong, CEO of Huawei’s Consumer Business Group, need to review documents while traveling.

# On Weibo, China’s equivalent of Twitter, the topic "Huawei trifold" (#华为三折叠#) quickly rose to the top of the Hot Search list, staying there for nearly 10 hours and amassing 300 million views. Meanwhile, the official hashtag "Huawei Mate XT Ultimate Design" (#华为MateXT非凡大师#) gained 290,000 views but only reached number 29 on the list. Another trending topic, about the phone being resold for 90,000 RMB ($12,641) on Goofish, ranked at number 8.

# Much of the online conversation has centered around whether the cutting-edge technology justifies the high price and who would be willing to spend 90,000 to 100,000 RMB on a smartphone. Many media outlets have also drawn comparisons between the iPhone 16 and Huawei's trifold device. Analysts suggest Huawei’s foray into the premium market is a strategic move to avoid direct competition with Apple’s iPhone 16, despite both being unveiled on the same day. However, the upcoming Mate 70 and the “pure blood” HarmonyOS, set for release in Q4, may pose a bigger challenge to Apple. """,
#         "main_image": "https://daoinsights.com/wp-content/uploads/2024/09/huawei-1-1536x660.jpg"  # URL of the uploaded image
#     }
# }

# response = requests.post(
#     f"https://api.webflow.com/collections/{collection_id}/items",
#     headers={
#         "Authorization": f"Bearer {api_key}",
#         "Content-Type": "application/json",
#         "accept-version": "1.0.0"
#     },
#     data=json.dumps(article_data)
# )

# # Check the response
# if response.status_code == 200:
#     print(f"Article created successfully: {response.json()}")
# else:
#     print(f"Failed to create article: {response.text}")
