import requests
import random
import time
from lxml import html

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

# File to store previously scraped URLs
url_storage_file = 'scraped_urls.json'

# Load previously scraped URLs
def load_scraped_urls():
    if os.path.exists(url_storage_file):
        with open(url_storage_file, 'r') as f:
            return json.load(f)
    return []

# Save scraped URLs to file
def save_scraped_urls(scraped_urls):
    with open(url_storage_file, 'w') as f:
        json.dump(scraped_urls, f)

# Scrape the homepage and get URLs
def get_new_urls():
    url = "https://daoinsights.com/"
    headers = {
        "User-Agent": random.choice(user_agents),
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com/"
    }
    
    try:
        response = requests.get(url, headers=headers)
        tree = html.fromstring(response.content)
        # Extract URLs of articles
        links = tree.xpath('//a[@class="preview-image"]/@href')
        return ["https://daoinsights.com" + link for link in links]
    except requests.exceptions.RequestException as e:
        print(f"Failed to get homepage: {e}")
        return []

# Scrape individual article for title, image, and text
def scrape_article(url):
    headers = {
        "User-Agent": random.choice(user_agents),
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com/"
    }

    time.sleep(random.uniform(1, 5))  # Delay before making request
    
    try:
        response = requests.get(url, headers=headers)
        print(f"Scraping {url}, Status Code: {response.status_code}")
        
        tree = html.fromstring(response.content)
        
        # Get title
        title = tree.xpath("//h1[@class='entry-title']/text()")
        title = title[0] if title else "No title found"
        
        # Get image URL
        img_url = tree.xpath("//div[@class='featured-media']/img/@src")
        img_url = img_url[0] if img_url else "No image found"
        
        # Get paragraphs
        paragraphs = tree.xpath('//p/text()')
        
        # Target text (stop extraction before this text)
        target_text = "© 2024 Dao Insights"
        
        extracted_paragraphs = []
        for p in paragraphs:
            if target_text in p:
                break
            extracted_paragraphs.append(p.strip())
        
        text = ''.join(extracted_paragraphs)
        
        return title, img_url, text[:100]  # Limit text for preview
    except requests.exceptions.RequestException as e:
        print(f"Failed to scrape {url}: {e}")
        return None, None, None

def parse():
    # Load previously scraped URLs
    scraped_urls = load_scraped_urls()
    
    # Get new URLs from the homepage
    new_urls = get_new_urls()
    
    # Prepare a list to store new articles
    new_articles = []
    
    # Compare and scrape new URLs
    for url in new_urls:
        if url not in scraped_urls:
            title, img_url, text = scrape_article(url)
            if title and img_url and text:
                new_articles.append({
                    "url": url,
                    "title": title,
                    "img_url": img_url,
                    "text": text
                })
                scraped_urls.append(url)  # Add new URL to the list

    # Save updated list of scraped URLs
    save_scraped_urls(scraped_urls)
    
    # Return the new articles
    return new_articles

