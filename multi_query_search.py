import requests
import json
import time

# Multiple specific search queries to get around the 1000 paper limit
search_queries = [
    '"generative ai"',
    '"generative artificial intelligence"',
    '"large language models"',
    '"LLM"',
    '"GPT"',
    '"BERT"',
    '"transformer models"',
    '"neural networks"',
    '"deep learning"',
    '"machine learning"'
]

# Different year ranges to get more papers
year_ranges = [
    "2023-",
    "2022-",
    "2021-",
    "2020-"
]

url = "http://api.semanticscholar.org/graph/v1/paper/search/bulk"

def search_papers(query, year_range, output_file):
    """Search for papers with a specific query and year range"""
    query_params = {
        "query": query,
        "fields": "title,url,publicationTypes,publicationDate,openAccessPdf,year,fieldsOfStudy",
        "year": year_range
    }
    
    print(f"\n🔍 Searching: {query} ({year_range})")
    
    response = requests.get(url, params=query_params).json()
    total_available = response.get('total', 0)
    print(f"📊 Papers available: {total_available}")
    
    if total_available == 0:
        return 0
    
    retrieved = 0
    batch_number = 1
    
    with open(output_file, "a") as file:
        while True:
            if "data" in response:
                batch_size = len(response["data"])
                retrieved += batch_size
                print(f"  Batch #{batch_number}: {batch_size} papers (Total: {retrieved})")
                
                for paper in response["data"]:
                    # Add query info to each paper for tracking
                    paper['search_query'] = query
                    paper['year_range'] = year_range
                    print(json.dumps(paper), file=file)
            
            if "token" not in response or response["token"] is None or retrieved >= 1000:
                break
                
            try:
                response = requests.get(f"{url}&token={response['token']}").json()
                batch_number += 1
            except Exception as e:
                print(f"    ❌ Error fetching next batch: {e}")
                print(f"    → Stopping this query due to API error")
                break
    
    print(f"  ✅ Retrieved {retrieved} papers for this query")
    return retrieved

# Main execution
if __name__ == "__main__":
    total_papers = 0
    output_file = "extended_papers.json"
    
    # Clear the output file
    with open(output_file, "w") as f:
        f.write("")
    
    print("🚀 Starting multi-query search to bypass 1000 paper limit...")
    print("=" * 60)
    
    for query in search_queries:
        for year_range in year_ranges:
            papers_found = search_papers(query, year_range, output_file)
            total_papers += papers_found
            
            # Small delay to be respectful to the API
            time.sleep(1)
    
    print("\n" + "=" * 60)
    print(f"🎯 Total papers retrieved across all queries: {total_papers}")
    print(f"💾 All papers saved to: {output_file}")
    print("\n💡 This approach bypasses the 1000 paper limit by using multiple search queries!")

