import requests
import json

# Test with a smaller query to see batching clearly
url = "http://api.semanticscholar.org/graph/v1/paper/search/bulk"

# Smaller query for testing
query_params = {
    "query": '"machine learning"',
    "fields": "title,year",
    "year": "2024-",
    "limit": 5  # Small limit to force multiple batches
}

print("🔍 Testing Semantic Scholar API pagination...")
print("=" * 50)

response = requests.get(url, params=query_params).json()
total_papers = response.get('total', 0)
print(f"📊 Total papers available: {total_papers}")

batch_number = 1
total_retrieved = 0

while True:
    if "data" in response:
        batch_size = len(response["data"])
        total_retrieved += batch_size
        
        print(f"\n📦 Batch #{batch_number}")
        print(f"   Papers in this batch: {batch_size}")
        print(f"   Total retrieved so far: {total_retrieved}")
        
        # Show sample titles from this batch
        for i, paper in enumerate(response["data"][:3]):  # Show first 3 titles
            title = paper.get('title', 'No title')
            year = paper.get('year', 'No year')
            print(f"   {i+1}. {title[:60]}... ({year})")
        
        if len(response["data"]) > 3:
            print(f"   ... and {len(response["data"]) - 3} more papers")
    
    # Check for continuation token
    if "token" in response:
        token_preview = response['token'][:30] + "..." if len(response['token']) > 30 else response['token']
        print(f"   🔑 Continuation token: {token_preview}")
        print(f"   ⏭️  Fetching next batch...")
        
        # Get next batch
        response = requests.get(f"{url}&token={response['token']}").json()
        batch_number += 1
    else:
        print(f"\n✅ No more tokens - pagination complete!")
        print(f"🎯 Final count: {total_retrieved} papers retrieved in {batch_number} batches")
        break

print("\n" + "=" * 50)
print("💡 This demonstrates how continuation tokens enable pagination!")
print("   Each token represents a 'bookmark' to the next batch of results.")
