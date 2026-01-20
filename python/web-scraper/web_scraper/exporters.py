"""Export scraped data to various formats"""
import json
import csv
import pandas as pd
from pathlib import Path
from typing import List
from web_scraper.models import ScrapeResult, ScrapedItem


class JSONExporter:
    """Export data to JSON"""
    
    @staticmethod
    def export(results: List[ScrapeResult], output_file: str):
        """Export to JSON file"""
        data = [result.to_dict() for result in results]
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Exported to JSON: {output_file}")


class CSVExporter:
    """Export data to CSV"""
    
    @staticmethod
    def export(results: List[ScrapeResult], output_file: str):
        """Export to CSV file"""
        # Flatten all items from all results
        rows = []
        for result in results:
            for item in result.items:
                row = item.to_dict()
                rows.append(row)
        
        if not rows:
            print("Warning: No data to export")
            return
        
        # Get all unique keys
        keys = set()
        for row in rows:
            keys.update(row.keys())
        
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=sorted(keys))
            writer.writeheader()
            writer.writerows(rows)
        
        print(f"✓ Exported to CSV: {output_file}")


class ExcelExporter:
    """Export data to Excel"""
    
    @staticmethod
    def export(results: List[ScrapeResult], output_file: str):
        """Export to Excel file"""
        # Create DataFrame for each result
        writer = pd.ExcelWriter(output_file, engine='openpyxl')
        
        for idx, result in enumerate(results):
            if not result.items:
                continue
            
            # Convert items to DataFrame
            data = [item.to_dict() for item in result.items]
            df = pd.DataFrame(data)
            
            # Create sheet name from URL
            sheet_name = f"Page_{idx + 1}"
            df.to_excel(writer, sheet_name=sheet_name, index=False)
        
        writer.close()
        print(f"✓ Exported to Excel: {output_file}")


class MarkdownExporter:
    """Export data to Markdown"""
    
    @staticmethod
    def export(results: List[ScrapeResult], output_file: str):
        """Export to Markdown file"""
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("# Scrape Results\n\n")
            
            for result in results:
                f.write(f"## {result.url}\n\n")
                f.write(f"- **Status**: {'✓ Success' if result.success else '✗ Failed'}\n")
                f.write(f"- **Items**: {len(result.items)}\n")
                f.write(f"- **Duration**: {result.duration:.2f}s\n\n")
                
                if result.error:
                    f.write(f"**Error**: {result.error}\n\n")
                
                for idx, item in enumerate(result.items, 1):
                    f.write(f"### Item {idx}: {item.title}\n\n")
                    for key, value in item.data.items():
                        f.write(f"- **{key}**: {value}\n")
                    f.write("\n")
        
        print(f"✓ Exported to Markdown: {output_file}")
