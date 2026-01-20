# Web Scraper Tool

A flexible web scraping tool with support for CSS selectors, XPath, and regex extraction with multiple export formats.

## ⚡ Quick Run

```bash
# 1. Setup environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 2. Try example scraper
python -m web_scraper.cli \
  --config examples/hacker_news.json \
  --output results.json \
  --format json

# 3. View results
cat results.json | python -m json.tool
```

## 🧪 Quick Examples

```bash
# Scrape Hacker News to JSON
python -m web_scraper.cli -c examples/hacker_news.json -o hn.json

# Export to CSV
python -m web_scraper.cli -c examples/hacker_news.json -o hn.csv --format csv

# Export to Excel
python -m web_scraper.cli -c examples/hacker_news.json -o hn.xlsx --format excel

# Scrape multiple pages with delay
python -m web_scraper.cli -c config.json -o results.json --max-pages 5 --delay 2.0
```

## Features

- ✅ Multiple extraction methods (CSS, XPath, Regex)
- ✅ Rate limiting and polite scraping
- ✅ Multiple export formats (JSON, CSV, Excel, Markdown)
- ✅ Link following for multi-page scraping
- ✅ Custom headers and user agents
- ✅ URL validation and normalization
- ✅ Error handling and retry logic

## Installation

1. **Create virtual environment**
   ```bash
   cd python/web-scraper
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Basic Scraping

```bash
# Scrape with config file
scraper --config examples/hacker_news.json --output results.json

# Export to different formats
scraper -c config.json -o results.csv --format csv
scraper -c config.json -o results.xlsx --format excel
scraper -c config.json -o results.md --format markdown

# Override config options
scraper -c config.json -o results.json --max-pages 5 --delay 2.0
```

### Configuration File Format

```json
{
  "url": "https://example.com",
  "selector_type": "css",
  "selectors": {
    "_container": ".item",
    "title": "h2.title",
    "link": "a.link@href",
    "description": "p.desc"
  },
  "max_pages": 1,
  "delay": 1.0,
  "user_agent": "Mozilla/5.0...",
  "headers": {
    "Accept": "text/html"
  },
  "follow_links": false,
  "link_selector": "a.next"
}
```

### Selector Types

**CSS Selectors:**
```json
{
  "selector_type": "css",
  "selectors": {
    "_container": ".article",
    "title": "h1",
    "link": "a@href",
    "content": ".content"
  }
}
```

**XPath:**
```json
{
  "selector_type": "xpath",
  "selectors": {
    "_container": "//div[@class='article']",
    "title": ".//h1/text()",
    "link": ".//a/@href"
  }
}
```

**Regex:**
```json
{
  "selector_type": "regex",
  "selectors": {
    "title": "<h1>(.*?)</h1>",
    "email": "([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,})"
  }
}
```

## Programmatic Usage

```python
from web_scraper.scraper import WebScraper
from web_scraper.models import ScrapeConfig
from web_scraper.exporters import JSONExporter

# Create configuration
config = ScrapeConfig(
    url="https://example.com",
    selector_type="css",
    selectors={
        "_container": ".item",
        "title": "h2",
        "link": "a@href"
    },
    max_pages=3,
    delay=1.0
)

# Create scraper
scraper = WebScraper(config)

# Run scraping
results = scraper.scrape()

# Export results
JSONExporter.export(results, "output.json")

# Access data
for result in results:
    print(f"URL: {result.url}")
    print(f"Items: {len(result.items)}")
    for item in result.items:
        print(f"  - {item.title}")
```

## Conversion Target

This application is designed to be converted to **Go with Colly framework**.

### Key Conversion Points:

1. **Python classes → Go structs**
   - ScrapeConfig → struct
   - ScrapedItem → struct
   - WebScraper → struct with methods

2. **BeautifulSoup → Colly/goquery**
   - CSS selectors → colly.OnHTML
   - HTML parsing → goquery API
   - Link extraction → colly.OnRequest

3. **Pandas → encoding/csv + Excel library**
   - DataFrame operations → manual CSV writing
   - Excel export → excelize library

4. **Rate limiting**
   - time.sleep() → time.Sleep()
   - Custom rate limiter → colly.Limit()

5. **Error handling**
   - try/except → if err != nil
   - Custom exceptions → error types

## Project Structure

```
web-scraper/
├── web_scraper/
│   ├── __init__.py
│   ├── cli.py           # Command-line interface
│   ├── scraper.py       # Main scraper logic
│   ├── models.py        # Data models
│   ├── extractors.py    # CSS/XPath/Regex extractors
│   ├── exporters.py     # Export formats
│   └── utils.py         # HTTP client, validators
├── examples/
│   ├── hacker_news.json
│   └── reddit.json
├── requirements.txt
├── pyproject.toml
└── README.md
```

## Example Output

**JSON:**
```json
[
  {
    "url": "https://news.ycombinator.com/",
    "success": true,
    "duration": 0.85,
    "items_count": 30,
    "items": [
      {
        "title": "Example Article",
        "url": "https://example.com/article",
        "score": "125"
      }
    ]
  }
]
```

**CSV:**
```csv
url,title,timestamp,score,author
https://example.com,Article 1,2024-01-01T10:00:00,125,user1
https://example.com,Article 2,2024-01-01T10:00:01,98,user2
```

## Best Practices

1. **Be Polite**: Use appropriate delays between requests
2. **Respect robots.txt**: Check site's scraping policy
3. **Use User-Agent**: Identify your scraper
4. **Handle Errors**: Implement retry logic for failed requests
5. **Cache Results**: Avoid re-scraping the same data
6. **Rate Limit**: Don't overwhelm servers

## License

This is a workshop example application.
