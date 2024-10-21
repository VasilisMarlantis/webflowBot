import requests
import random
from lxml import html
import json
from datetime import datetime, timedelta
import os
import time

# List of 30 User-Agents for rotation
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.1 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15A372 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15A5341f Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 13_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 13_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.1 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 13_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 10; SM-G973U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.105 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 14_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15"
]

def parse(url):
    # Set custom headers
    headers = {
        "User-Agent": random.choice(user_agents),  # Rotate user-agent
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com/",  # Mimic referral from a trusted source
    }
    
    # Delay before making a request to avoid bot detection
    time.sleep(random.uniform(1, 5))  # Delay between 1 to 5 seconds
    
    # Send the request
    try:
        response = requests.get(url, headers=headers)
        
        # Print status code
        print(f"Status Code: {response.status_code}")
        
        # Parse the response content
        tree = html.fromstring(response.content)
        
        # Get title
        title = tree.xpath("//h1[@class='entry-title']/text()")
        title = title[0] if title else None  # Get first element or None
        
        # Get img url
        #get img url
        img_urls = tree.xpath("//div[@class='featured-media']/img/@src | //img[contains(@class, 'wp-image')]/@src")
        if(img_urls):
            for img_url in img_urls:
                print('img_url',img_url)          
            
            img_url = img_urls
        
        # Get all <p> tags
        paragraphs = tree.xpath('//p/text()')
        
        # Identify the target text
        target_text = "© 2024 Dao Insights"
        
        # Extract paragraphs until the target text is found
        extracted_paragraphs = []
        for p in paragraphs:
            if target_text in p:
                break
            extracted_paragraphs.append(p.strip())
        
        # Clean up the paragraphs and separate them with new lines
        text = ' '.join([p for p in extracted_paragraphs if p])
        
        # Return extracted text, img_url, and title
        return text, img_url, title
    
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None, None, None


def parse_urls():
    # Set headers for the request
    headers = {
        "User-Agent": random.choice(user_agents),
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com/"
    }

    # Fetch the webpage
    response = requests.get('https://daoinsights.com/', headers=headers)
    tree = html.fromstring(response.content)

    # Get today's date
    today = datetime(2024, 10, 16).strftime("%B %d, %Y")  # Example: "October 19, 2024"

    # Define the filename
    filename = 'urls_data.json'

    # Check if the file exists
    file_exists = os.path.exists(filename)
    if file_exists:
        with open(filename, 'r', encoding='utf-8') as f:
            try:
                existing_data = json.load(f)
            except json.JSONDecodeError:
                existing_data = {'urls_data': []}
    else:
        existing_data = {'urls_data': []}

    # Ensure 'urls_data' key exists
    if 'urls_data' not in existing_data:
        existing_data['urls_data'] = []

    # Check if today's date is in the file
    dates_in_file = {entry['date'] for entry in existing_data['urls_data']}

    if today not in dates_in_file:
        # If today's date is not in the file, delete the file
        if file_exists:
            os.remove(filename)
            print(f"Deleted {filename} as today's date ({today}) was not found.")

        # Reset existing_data after file deletion
        existing_data = {'urls_data': []}

    # Extract URLs for posts
    posts = tree.xpath('//a[@class="meta-wrapper"]')
    extracted_urls = []

    for post in posts:
        url = post.xpath('./@href')[0]  # Extract URL
        date = post.xpath('.//span[@class="screen-reader-text"]/following-sibling::text()')[0].strip()  # Extract post date

        # Check if the date matches today
        if date == today:
            extracted_urls.append({"url": url, "date": today})

    # Find new URLs by comparing with the existing ones saved today
    existing_urls_today = [entry['url'] for entry in existing_data['urls_data'] if entry['date'] == today]
    new_urls = [entry for entry in extracted_urls if entry['url'] not in existing_urls_today]

    # If there are new URLs, update the file and return them
    if new_urls:
        # Add the new URLs to the existing data
        existing_data['urls_data'].extend(new_urls)

        # Save the updated data back to the file
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, indent=4)

        print(f"New URLs added and saved to {filename}: {new_urls}")

        # Now loop through each new URL and use the parse function
        parsed_results = []
        for entry in new_urls:
            url = entry['url']
            text, img_url, title = parse(url)  # Parse each URL
            if text or img_url or title:  # If at least some data was extracted
                parsed_results.append([text, img_url, title])
        
        return parsed_results  # Return the parsed data
    
    else:
        # If no new URLs, save the file with today's date even if no URLs were found
        if not file_exists or len(existing_data['urls_data']) == 0:
            existing_data['urls_data'].append({"url": None, "date": today})
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(existing_data, f, indent=4)

            print(f"No new URLs, but file created/updated with today's date: {today}.")
        else:
            print("No new URLs to add and the file already contains today's data.")

        return []  # Return an empty list if no new URLs

