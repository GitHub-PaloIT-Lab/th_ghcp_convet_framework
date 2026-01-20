"""Data models for web scraping"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Any, Optional


@dataclass
class ScrapedItem:
    """Single scraped item"""
    url: str
    title: str
    data: Dict[str, Any]
    timestamp: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'url': self.url,
            'title': self.title,
            'timestamp': self.timestamp.isoformat(),
            **self.data
        }


@dataclass
class ScrapeResult:
    """Result of scraping operation"""
    url: str
    items: List[ScrapedItem]
    success: bool
    error: Optional[str] = None
    duration: float = 0.0  # seconds
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'url': self.url,
            'success': self.success,
            'error': self.error,
            'duration': self.duration,
            'items_count': len(self.items),
            'items': [item.to_dict() for item in self.items]
        }


@dataclass
class ScrapeConfig:
    """Configuration for scraping"""
    url: str
    selector_type: str  # css, xpath, or regex
    selectors: Dict[str, str]
    max_pages: int = 1
    delay: float = 1.0  # seconds between requests
    user_agent: Optional[str] = None
    headers: Dict[str, str] = field(default_factory=dict)
    follow_links: bool = False
    link_selector: Optional[str] = None
