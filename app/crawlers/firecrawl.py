from typing import List, Dict, Optional
import trafilatura
import requests
from bs4 import BeautifulSoup
from langchain.text_splitter import RecursiveCharacterTextSplitter
from urllib.parse import urljoin, urlparse

class Firecrawl:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )

    def extract_content(self, url: str) -> Optional[str]:
        """Extract main content from a webpage."""
        try:
            downloaded = trafilatura.fetch_url(url)
            if downloaded:
                return trafilatura.extract(downloaded)
            return None
        except Exception as e:
            print(f"Error extracting content from {url}: {str(e)}")
            return None

    def get_links(self, url: str, base_domain: Optional[str] = None) -> List[str]:
        """Get all links from a webpage, optionally filtered by domain."""
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            links = []
            
            for link in soup.find_all('a'):
                href = link.get('href')
                if href:
                    full_url = urljoin(url, href)
                    if base_domain:
                        if urlparse(full_url).netloc == base_domain:
                            links.append(full_url)
                    else:
                        links.append(full_url)
            
            return list(set(links))
        except Exception as e:
            print(f"Error getting links from {url}: {str(e)}")
            return []

    def crawl_website(self, url: str, max_pages: int = 10, same_domain: bool = True) -> List[Dict]:
        """Crawl a website and extract content from its pages."""
        visited = set()
        to_visit = [url]
        results = []
        base_domain = urlparse(url).netloc if same_domain else None

        while to_visit and len(visited) < max_pages:
            current_url = to_visit.pop(0)
            if current_url in visited:
                continue

            content = self.extract_content(current_url)
            if content:
                chunks = self.text_splitter.split_text(content)
                results.append({
                    "url": current_url,
                    "content": content,
                    "chunks": chunks
                })

            visited.add(current_url)
            
            # Get new links to visit
            new_links = self.get_links(current_url, base_domain)
            to_visit.extend([link for link in new_links if link not in visited])

        return results 