"""Command-line interface for web scraper"""
import argparse
import json
from pathlib import Path
from web_scraper.scraper import WebScraper
from web_scraper.models import ScrapeConfig
from web_scraper.exporters import JSONExporter, CSVExporter, ExcelExporter, MarkdownExporter


def load_config_file(config_path: str) -> ScrapeConfig:
    """Load configuration from JSON file"""
    with open(config_path, 'r') as f:
        data = json.load(f)
    
    return ScrapeConfig(
        url=data['url'],
        selector_type=data.get('selector_type', 'css'),
        selectors=data['selectors'],
        max_pages=data.get('max_pages', 1),
        delay=data.get('delay', 1.0),
        user_agent=data.get('user_agent'),
        headers=data.get('headers', {}),
        follow_links=data.get('follow_links', False),
        link_selector=data.get('link_selector')
    )


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(description='Web Scraper Tool')
    
    # Input options
    parser.add_argument('--config', '-c', required=True, 
                       help='Path to configuration JSON file')
    
    # Output options
    parser.add_argument('--output', '-o', required=True,
                       help='Output file path')
    parser.add_argument('--format', '-f', 
                       choices=['json', 'csv', 'excel', 'markdown'],
                       default='json',
                       help='Output format')
    
    # Scraping options
    parser.add_argument('--max-pages', type=int,
                       help='Maximum pages to scrape (overrides config)')
    parser.add_argument('--delay', type=float,
                       help='Delay between requests in seconds (overrides config)')
    
    args = parser.parse_args()
    
    # Load configuration
    print(f"📄 Loading configuration from {args.config}")
    config = load_config_file(args.config)
    
    # Override with CLI arguments
    if args.max_pages:
        config.max_pages = args.max_pages
    if args.delay:
        config.delay = args.delay
    
    # Create scraper
    print(f"🕷️  Starting scraper for {config.url}")
    scraper = WebScraper(config)
    
    # Run scraping
    results = scraper.scrape()
    
    # Print summary
    total_items = sum(len(r.items) for r in results)
    successful = sum(1 for r in results if r.success)
    print(f"\n📊 Scraping complete:")
    print(f"  - Pages: {len(results)} ({successful} successful)")
    print(f"  - Items: {total_items}")
    
    # Export results
    print(f"\n💾 Exporting to {args.format}...")
    
    if args.format == 'json':
        JSONExporter.export(results, args.output)
    elif args.format == 'csv':
        CSVExporter.export(results, args.output)
    elif args.format == 'excel':
        ExcelExporter.export(results, args.output)
    elif args.format == 'markdown':
        MarkdownExporter.export(results, args.output)
    
    print("\n✅ Done!")


if __name__ == '__main__':
    main()
