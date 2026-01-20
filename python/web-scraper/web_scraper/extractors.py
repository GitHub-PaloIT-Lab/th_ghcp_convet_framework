"""CSS selector-based extractor"""
from bs4 import BeautifulSoup
from typing import Dict, List, Any
from web_scraper.models import ScrapedItem


class CSSExtractor:
    """Extract data using CSS selectors"""
    
    def extract(self, html: str, url: str, selectors: Dict[str, str]) -> List[ScrapedItem]:
        """Extract data using CSS selectors"""
        soup = BeautifulSoup(html, 'lxml')
        items = []
        
        # Find all container elements (if specified)
        container_selector = selectors.get('_container', None)
        if container_selector:
            containers = soup.select(container_selector)
        else:
            containers = [soup]  # Use whole document
        
        for container in containers:
            data = {}
            title = ""
            
            for key, selector in selectors.items():
                if key.startswith('_'):  # Skip special keys
                    continue
                
                element = container.select_one(selector)
                if element:
                    # Extract text or attribute
                    if '@' in selector:  # Attribute selector
                        attr = selector.split('@')[1]
                        data[key] = element.get(attr, '')
                    else:
                        data[key] = element.get_text(strip=True)
                    
                    if key == 'title':
                        title = data[key]
            
            if data:  # Only add if we extracted something
                items.append(ScrapedItem(
                    url=url,
                    title=title or f"Item from {url}",
                    data=data
                ))
        
        return items


class XPathExtractor:
    """Extract data using XPath expressions"""
    
    def extract(self, html: str, url: str, selectors: Dict[str, str]) -> List[ScrapedItem]:
        """Extract data using XPath"""
        from lxml import html as lxml_html
        
        tree = lxml_html.fromstring(html)
        items = []
        
        # Find containers
        container_xpath = selectors.get('_container', '//*')
        containers = tree.xpath(container_xpath)
        
        if not containers:
            containers = [tree]
        
        for container in containers:
            data = {}
            title = ""
            
            for key, xpath in selectors.items():
                if key.startswith('_'):
                    continue
                
                try:
                    results = container.xpath(xpath)
                    if results:
                        if isinstance(results[0], str):
                            data[key] = results[0]
                        else:
                            data[key] = results[0].text_content().strip()
                        
                        if key == 'title':
                            title = data[key]
                except Exception:
                    continue
            
            if data:
                items.append(ScrapedItem(
                    url=url,
                    title=title or f"Item from {url}",
                    data=data
                ))
        
        return items


class RegexExtractor:
    """Extract data using regular expressions"""
    
    def extract(self, html: str, url: str, patterns: Dict[str, str]) -> List[ScrapedItem]:
        """Extract data using regex patterns"""
        import re
        
        data = {}
        title = ""
        
        for key, pattern in patterns.items():
            if key.startswith('_'):
                continue
            
            match = re.search(pattern, html, re.DOTALL)
            if match:
                data[key] = match.group(1) if match.groups() else match.group(0)
                if key == 'title':
                    title = data[key]
        
        items = []
        if data:
            items.append(ScrapedItem(
                url=url,
                title=title or f"Item from {url}",
                data=data
            ))
        
        return items
