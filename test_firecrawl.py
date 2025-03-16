import requests
import json

def test_single_page():
    print("\nTesting single page extraction...")
    response = requests.get(
        "http://localhost:8000/firecrawl/extract",
        params={"url": "https://python.org"}
    )
    result = response.json()
    print(f"Status Code: {response.status_code}")
    print(f"Content length: {len(result['content'])} characters")
    print(f"Number of chunks: {len(result['chunks'])}")
    print("\nFirst chunk preview:")
    print(result['chunks'][0][:200] + "...")

def test_multi_page():
    print("\nTesting multi-page crawling...")
    response = requests.post(
        "http://localhost:8000/firecrawl/crawl",
        json={
            "url": "https://python.org",
            "max_pages": 3,
            "same_domain": True
        }
    )
    results = response.json()
    print(f"Status Code: {response.status_code}")
    print(f"Number of pages crawled: {len(results)}")
    for i, result in enumerate(results):
        print(f"\nPage {i+1}:")
        print(f"URL: {result['url']}")
        print(f"Content length: {len(result['content'])} characters")
        print(f"Number of chunks: {len(result['chunks'])}")

if __name__ == "__main__":
    print("Testing Firecrawl API...")
    test_single_page()
    test_multi_page() 