"""SQLite-based cache for weather data"""
import sqlite3
from datetime import datetime, timedelta
from typing import Optional
import json
from pathlib import Path


class WeatherCache:
    """SQLite-based cache for weather data"""
    
    def __init__(self, db_path: str = "weather_cache.db"):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        """Initialize database schema"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS cache (
                    location TEXT PRIMARY KEY,
                    data TEXT NOT NULL,
                    cached_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
    
    def get(self, location: str, max_age: timedelta = timedelta(hours=1)) -> Optional[dict]:
        """Get cached weather data if not expired"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT data, cached_at FROM cache WHERE location = ?",
                (location.lower(),)
            )
            row = cursor.fetchone()
            
            if not row:
                return None
            
            data_json, cached_at_str = row
            cached_at = datetime.fromisoformat(cached_at_str)
            
            # Check if expired
            if datetime.now() - cached_at > max_age:
                return None
            
            return json.loads(data_json)
    
    def set(self, location: str, data: dict):
        """Cache weather data"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT OR REPLACE INTO cache (location, data, cached_at) VALUES (?, ?, ?)",
                (location.lower(), json.dumps(data), datetime.now().isoformat())
            )
            conn.commit()
    
    def clear_expired(self, max_age: timedelta = timedelta(hours=1)):
        """Remove expired cache entries"""
        cutoff = (datetime.now() - max_age).isoformat()
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DELETE FROM cache WHERE cached_at < ?", (cutoff,))
            conn.commit()
