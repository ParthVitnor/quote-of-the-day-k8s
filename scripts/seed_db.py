"""
Database seed script for Quote of the Day.
Reads quotes from data/quotes.yaml and populates the database.
"""
import os
import sys
import yaml

# Add parent directory to path to import app modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import get_db_context
from app.models import Quote
from app.config import settings


def load_quotes_from_yaml():
    """Load quotes from YAML file."""
    yaml_path = os.path.join(settings.DATA_DIR, "quotes.yaml")
    
    if not os.path.exists(yaml_path):
        print(f"Error: {yaml_path} not found")
        sys.exit(1)
    
    with open(yaml_path, 'r', encoding='utf-8') as file:
        data = yaml.safe_load(file) or {}
        return data.get('quotes', [])


def seed_database():
    """Seed the database with quotes from YAML file."""
    print("Starting database seed...")
    
    # Load quotes from YAML
    quotes = load_quotes_from_yaml()
    
    if not quotes:
        print("Error: No quotes found in YAML file")
        sys.exit(1)
    
    print(f"Found {len(quotes)} quotes in YAML file")
    
    # Connect to database and insert quotes
    with get_db_context() as db:
        # Load existing quotes into memory for deduplication
        existing = {(q.text, q.author) for q in db.query(Quote).all()}
        
        # Insert quotes
        inserted_count = 0
        skipped_count = 0
        
        for quote_data in quotes:
            text = (quote_data.get('text') or '').strip()
            author = (quote_data.get('author') or '').strip()
            
            if not text or not author:
                skipped_count += 1
                continue
            
            # Check if quote already exists in memory set
            if (text, author) in existing:
                skipped_count += 1
                continue
            
            # Insert new quote
            new_quote = Quote(text=text, author=author)
            db.add(new_quote)
            existing.add((text, author))
            inserted_count += 1
        
        # Commit all inserts
        db.commit()
        
        print(f"Inserted: {inserted_count}, Skipped: {skipped_count}")


if __name__ == "__main__":
    try:
        seed_database()
    except Exception as e:
        print(f"Error during seeding: {e}")
        sys.exit(1)
