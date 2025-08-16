import requests
import json

# Define the API endpoint URL
url = "http://api.semanticscholar.org/graph/v1/paper/search/bulk"

# Define the query parameters - using broader terms that researchers actually use
# Search Strategy: Use two separate quoted phrases to find papers that contain BOTH terms
# This is more effective than a single complex phrase like "generative ai in computer vision"
query_params = {
    "query": '"generative AI" "computer vision"',
    "fields": "title,url,publicationTypes,publicationDate,openAccessPdf,year,fieldsOfStudy",
    "year": "2023-"
}

print("🔍 Searching for: Generative AI approaches in Computer Vision")
print("📝 Query: 'generative AI' + 'computer vision' (2023 onwards)")
print("💡 This broader search will find papers discussing both topics together")
print("=" * 60)

# Send the API request
try:
    response = requests.get(url, params=query_params).json()
    
    # Validate response
    if not isinstance(response, dict):
        print("❌ Invalid response format from API")
        exit(1)
    
    if 'total' not in response:
        print("❌ No 'total' field in API response")
        exit(1)
        
    print(f"Will retrieve an estimated {response['total']} documents")
except Exception as e:
    print(f"❌ Error making API request: {e}")
    exit(1)
print(f"⚠️  Due to API limits, maximum 1000 papers will be retrieved")
retrieved = 0
batch_number = 1

# Write results to json file and get next batch of results
with open(f"papers.json", "a") as file:
    while True:
        if "data" in response and response["data"]:
            batch_size = len(response["data"])
            retrieved += batch_size
            print(f"Batch #{batch_number}: Retrieved {batch_size} papers (Total: {retrieved})")
            
            # Show token info for debugging
            if "token" in response and response["token"]:
                print(f"  → Continuation token: {response['token'][:20]}...")
            else:
                print(f"  → No more tokens - this is the final batch")
            
            for paper in response["data"]:
                print(json.dumps(paper), file=file)
        else:
            print(f"  ⚠️  No data in response for batch #{batch_number}")
            break
        
        # Stop at 1000 papers due to API limit
        if retrieved >= 1000:
            print(f"\n⚠️  Reached 1000 paper limit - API restriction")
            break
            
        # checks for continuation token to get next batch of results
        if "token" not in response or response["token"] is None:
            print(f"\n✅ All batches complete! Retrieved {retrieved} papers total")
            break
        
        print(f"  → Fetching next batch with token...")
        try:
            response = requests.get(f"{url}&token={response['token']}").json()
            batch_number += 1
        except Exception as e:
            print(f"  ❌ Error fetching next batch: {e}")
            print(f"  → Stopping due to API error")
            break

print(f"\n📊 Final result: {retrieved} papers retrieved")
print("💡 To get more papers, run: python multi_query_search.py")