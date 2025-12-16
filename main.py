import os
import requests
from dotenv import load_dotenv

load_dotenv()

ZOTERO_API=os.getenv("API_BASE_URL")
ZOTERO_API_USER=os.getenv("API_USER")
ZOTERO_API_TOKEN=os.getenv("API_TOKEN")

headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Zotero-API-Key': ZOTERO_API_TOKEN,
    'Zotero-API-Version': '3'
}

def zotero(endpoint):
  try:
    # Make request to the correct endpoint, not the base URL
    response = requests.get(f"{ZOTERO_API}/users/{ZOTERO_API_USER}" + endpoint, headers=headers)
    
    print(f"status: {response.status_code}")
    
    # Check if response is valid before trying to parse JSON
    if response.status_code == 200:
        try:
            return response.json()
        except ValueError as e:
            print(f"JSON decode error: {e}")
            print(f"Response content: {response.text}")
    else:
        print(f"Request failed with status code: {response.status_code}")
        print(f"Response content: {response.text}")
        
  except requests.exceptions.RequestException as e:
      print(f"Request error: {e}")

def fetch_tags():
  tags = []
  for t in zotero("/tags?limit=100"):
     tags.append({"name": t['tag'], "annotations": t['meta']['numItems']})
  
  return tags

def fetch_items():
   data = zotero("/items?limit=100")
   return data

def get_items_for_tag(tag):
   items_with_tag = []
   
   for item in fetch_items():
      tags = [t['tag'] for t in item['data']['tags']]

      for t in tags:
         if tag.lower() == t.lower():
            items_with_tag.append(item)
   
   result = []
   for item in items_with_tag:
      result.append({
        "page":  item['data']['annotationPageLabel'],
        "text":  item['data']['annotationText'],
        "comment":  item['data']['annotationComment'],
        "tags":  tags
      })

   return result

#tags = fetch_tags()
#print(f"total tags: {len(tags)}")
#print(tags)

#items = fetch_items()
#print(f"total: {len(items)}")
#print(items)

tag="soa"
items=get_items_for_tag("soa")
print(f"total: {len(items)}")
print(f"tag: {tag}")
print(items)