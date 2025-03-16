from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, HttpUrl
from typing import List, Optional
from ..crawlers.firecrawl import Firecrawl

router = APIRouter(
    prefix="/firecrawl",
    tags=["firecrawl"],
)

class CrawlRequest(BaseModel):
    url: HttpUrl
    max_pages: Optional[int] = 10
    same_domain: Optional[bool] = True

class CrawlResponse(BaseModel):
    url: str
    content: str
    chunks: List[str]

@router.post("/crawl", response_model=List[CrawlResponse])
async def crawl_website(request: CrawlRequest):
    """
    Crawl a website and extract its content.
    
    - url: The starting URL to crawl
    - max_pages: Maximum number of pages to crawl (default: 10)
    - same_domain: Whether to stay on the same domain (default: True)
    """
    try:
        crawler = Firecrawl()
        results = crawler.crawl_website(
            str(request.url),
            max_pages=request.max_pages,
            same_domain=request.same_domain
        )
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/extract", response_model=CrawlResponse)
async def extract_single_page(url: HttpUrl):
    """
    Extract content from a single webpage.
    
    - url: The URL to extract content from
    """
    try:
        crawler = Firecrawl()
        content = crawler.extract_content(str(url))
        if not content:
            raise HTTPException(status_code=404, detail="No content found")
        
        chunks = crawler.text_splitter.split_text(content)
        return {
            "url": str(url),
            "content": content,
            "chunks": chunks
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 