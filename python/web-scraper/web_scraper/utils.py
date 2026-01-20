"""HTTP client with rate limiting and retries"""
import requests
import time
from typing import Optional, Dict
from urllib.parse import urljoin, urlparse


class HTTPClient:
    """HTTP client with rate limiting"""
    
    def __init__(self, delay: float = 1.0, user_agent: Optional[str] = None):
        self.delay = delay
        self.last_request_time = 0.0
        self.session = requests.Session()
        
        if user_agent:
            self.session.headers['User-Agent'] = user_agent
        else:
            self.session.headers['User-Agent'] = (
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            )
    
    def get(self, url: str, headers: Optional[Dict[str, str]] = None) -> requests.Response:
        """Make GET request with rate limiting"""
        self._rate_limit()
        
        try:
            response = self.session.get(
                url,
                headers=headers or {},
                timeout=30,
                allow_redirects=True
            )
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            raise RuntimeError(f"HTTP request failed for {url}: {e}") from e
    
    def _rate_limit(self):
        """Enforce rate limiting"""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.delay:
            time.sleep(self.delay - elapsed)
        self.last_request_time = time.time()


class URLValidator:
    """Validate and normalize URLs"""
    
    @staticmethod
    def is_valid(url: str) -> bool:
        """Check if URL is valid"""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except Exception:
            return False
    
    @staticmethod
    def normalize(url: str, base_url: str = "") -> str:
        """Normalize URL (handle relative URLs)"""
        if base_url:
            return urljoin(base_url, url)
        return url
    
    @staticmethod
    def same_domain(url1: str, url2: str) -> bool:
        """Check if two URLs are from same domain"""
        return urlparse(url1).netloc == urlparse(url2).netloc
