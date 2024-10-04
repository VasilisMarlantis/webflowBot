from scraper import parse

import requests
import json
from datetime import datetime, timedelta
import os
# Webflow API details

API_KEY = '13ff929739596aa0d9c8e160be497ee4822f93833420ea36d998ce8c1bf2c964'
SITE_ID = '651edd4c0bcc2eb5950e53da'    
COLLECTION_ID = "6553e71600ad68934cb80cb0"



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


if __name__ == "__main__":
    parse()