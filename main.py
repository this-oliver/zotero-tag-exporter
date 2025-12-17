import os
import time
import argparse
import requests
from dotenv import load_dotenv

load_dotenv()

ZOTERO_API="https://api.zotero.org"
ZOTERO_API_USER=os.getenv("USER_ID")
ZOTERO_API_TOKEN=os.getenv("TOKEN")

headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Zotero-API-Key': ZOTERO_API_TOKEN,
    'Zotero-API-Version': '3'
}

def zotero(endpoint):
  """
  Docstring for zotero
  
  :param endpoint: Endpoint to the zotero api excluding the base url.
  """
  try:
    # Make request to the correct endpoint, not the base URL
    response = requests.get(f"{ZOTERO_API}/users/{ZOTERO_API_USER}" + endpoint, headers=headers)
    
    if debug == True:
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
        print(f"Response header: {response.headers}")
        print(f"Response content: {response.text}")
        
  except requests.exceptions.RequestException as e:
      print(f"Request error: {e}")

def fetch_tags(limit=100):
  """
  Docstring for fetch_tags
  
  :param limit: An int between 1-100. Default is 100.
  """
  tags = []
  for t in zotero(f"/tags?limit={limit}"):
     tags.append({"name": t['tag'], "annotations": t['meta']['numItems']})
  
  return tags

def fetch_items(limit=100, include="data"):
   """
   Docstring for fetch_items
   
   :param limit: An int between 1-100. Default is 100.
   :param include: Description
   """
   data = zotero(f"/items?limit={limit}&include={include}")
   return data

def fetch_items_by_tag(tag):
   """
   Docstring for fetch_items_by_tag
   
   :param tag: Tag to filter PDFs and Articles by
   """
   items_with_tag = []
   
   for item in fetch_items():
      tags = [t['tag'] for t in item['data']['tags']]

      for t in tags:
         if tag.lower() == t.lower():
            items_with_tag.append(item)
   
   result = []
   for item in items_with_tag:
      annotation = {
        "page":  item['data']['annotationPageLabel'],
        "text":  item['data']['annotationText'],
        "comment":  item['data']['annotationComment'],
        "tags":  tags
      }

      ancestors = []
      
      # fetch extra stuff here
      if item['data']['itemType'] == 'annotation':
         pdf=None
         article=None

         for ancestor in ancestors:
            if ancestor['pdf']['key'] == item['data']['parentItem']:
               pdf = ancestor['pdf']
               article = ancestor['article']
               break
            
         if pdf is None and item['data']['parentItem']:
          pdf=zotero(f"/items/{item['data']['parentItem']}")
          article=zotero(f"/items/{pdf['data']['parentItem']}")
          ancestors.append({"pdf": pdf, "article": article})

         if pdf and article:
          annotation['authors'] = [a['lastName'] for a in article['data']['creators']]
          annotation['title'] = article['data']['title']
          annotation['date'] = article['data']['date']

      result.append(annotation)

   return result

def main():
  parser = argparse.ArgumentParser(prog="zotero exporter", description="exports stuff from zotero")
  parser.add_argument('--tag', '-t', help="tag to extract annotations from", action="extend", nargs="+", type=str, dest="tag", required=True)
  parser.add_argument('-d', '--debug', help="log debug info", action="store_true", dest="debug", default=False)
  
  args = parser.parse_args()
  tags = args.tag

  if tags is None or len(tags) == 0:
     parser.print_help()
     exit(1)

  stopwatch_start = time.time()
  results = [];
  content = f"\n# annotations by tags\n"
  
  for tag in tags:
    items=fetch_items_by_tag(tag)
    results.append({"tag": tag, "items": items})
    content += f"\n## {tag}\n"
    
    for item in items:
      metadata = f"{', '.join(item['authors'])}, {item['date']}, p.{item['page']}"
      content += f"\n{item['text']} ({metadata}) {', '.join(item['tags'])}\n\n"

  stopwatch_stop = time.time()
  
  total = 0
  for r in results:
      total = total + len(r['items'])

  print(content)
  print(f"==== found {total} annotations for [{', '.join(tags)}] tags in {stopwatch_stop - stopwatch_start:.2} seconds ====")

if __name__ == "__main__":
   main()