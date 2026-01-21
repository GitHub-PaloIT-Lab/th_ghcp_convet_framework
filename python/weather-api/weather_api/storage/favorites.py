"""Favorites location manager"""
import sqlite3
from typing import List


class FavoritesManager:
    """Manager for favorite locations"""
    
    def __init__(self, db_path: str = "weather_cache.db"):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        """Initialize favorites table"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS favorites (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    location TEXT UNIQUE NOT NULL,
                    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
    
    def add(self, location: str):
        """Add a location to favorites"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("INSERT INTO favorites (location) VALUES (?)", (location,))
                conn.commit()
        except sqlite3.IntegrityError:
            raise ValueError(f"'{location}' is already in favorites")
    
    def remove(self, location: str) -> bool:
        """Remove a location from favorites"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("DELETE FROM favorites WHERE location = ?", (location,))
            conn.commit()
            return cursor.rowcount > 0
    
    def list(self) -> List[str]:
        """List all favorite locations"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT location FROM favorites ORDER BY location")
            return [row[0] for row in cursor.fetchall()]
