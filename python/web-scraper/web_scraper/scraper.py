"""Main web scraper implementation"""
import time
from typing import List, Optional
from bs4 import BeautifulSoup
from web_scraper.models import ScrapeConfig, ScrapeResult, ScrapedItem
from web_scraper.extractors import CSSExtractor, XPathExtractor, RegexExtractor
from web_scraper.utils import HTTPClient, URLValidator


class WebScraper:
    """Main web scraper class"""
    
    def __init__(self, config: ScrapeConfig):
        self.config = config
        self.client = HTTPClient(
            delay=config.delay,
            user_agent=config.user_agent
        )
        self.extractor = self._get_extractor(config.selector_type)
        self.visited_urls = set()
    
    def scrape(self) -> List[ScrapeResult]:
        """Perform scraping operation"""
        results = []
        urls_to_visit = [self.config.url]
        
        for _ in range(self.config.max_pages):
            if not urls_to_visit:
                break
            
            url = urls_to_visit.pop(0)
            if url in self.visited_urls:
                continue
            
            result = self._scrape_page(url)
            results.append(result)
            self.visited_urls.add(url)
            
            # Find more links if configured
            if self.config.follow_links and result.success:
                new_urls = self._extract_links(url, result.items)
                urls_to_visit.extend(new_urls)
        
        return results
    
    def _scrape_page(self, url: str) -> ScrapeResult:
        """Scrape a single page"""
        start_time = time.time()
        
        try:
            # Validate URL
            if not URLValidator.is_valid(url):
                raise ValueError(f"Invalid URL: {url}")
            
            # Fetch page
            response = self.client.get(url, headers=self.config.headers)
            html = response.text
            
            # Extract data
            items = self.extractor.extract(
                html=html,
                url=url,
                selectors=self.config.selectors
            )
            
            duration = time.time() - start_time
            
            return ScrapeResult(
                url=url,
                items=items,
                success=True,
                duration=duration
            )
            
        except Exception as e:
            duration = time.time() - start_time
            return ScrapeResult(
                url=url,
                items=[],
                success=False,
                error=str(e),
                duration=duration
            )
    
    def _extract_links(self, base_url: str, items: List[ScrapedItem]) -> List[str]:
        """Extract links from scraped items"""
        if not self.config.link_selector:
            return []
        
        links = []
        for item in items:
            # Look for link in data
            for value in item.data.values():
                if isinstance(value, str) and value.startswith('http'):
                    # Normalize and validate
                    normalized = URLValidator.normalize(value, base_url)
                    if (URLValidator.is_valid(normalized) and 
                        URLValidator.same_domain(base_url, normalized) and
                        normalized not in self.visited_urls):
                        links.append(normalized)
        
        return links
    
    def _get_extractor(self, selector_type: str):
        """Get appropriate extractor"""
        if selector_type == 'css':
            return CSSExtractor()
        elif selector_type == 'xpath':
            return XPathExtractor()
        elif selector_type == 'regex':
            return RegexExtractor()
        else:
            raise ValueError(f"Unknown selector type: {selector_type}")
