"""
Quote rotation script for Quote of the Day.
Selects the next quote sequentially and sets it as today's quote.
Runs daily as a Kubernetes CronJob.
"""
import os
import sys
from datetime import date

# Add parent directory to path to import app modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import get_db_context
from app.models import Quote, DailyQuote


def rotate_quote():
    """Select next quote sequentially and set as today's quote."""
    today = date.today()
    
    with get_db_context() as db:
        # Check if today's quote already exists
        existing_daily = db.query(DailyQuote).filter(DailyQuote.date == today).first()
        
        if existing_daily:
            print("Quote already set for today")
            return
        
        # Get total number of quotes
        total_quotes = db.query(Quote).count()
        
        if total_quotes == 0:
            print("Error: No quotes in database")
            sys.exit(1)
        
        # Get last used quote to determine next one
        last_daily = db.query(DailyQuote).order_by(DailyQuote.date.desc()).first()
        
        if last_daily:
            # Sequential selection: get next quote
            last_quote_id = last_daily.quote_id
            next_quote = db.query(Quote).filter(Quote.id > last_quote_id).order_by(Quote.id).first()
            
            # If no next quote found, loop back to first quote
            if not next_quote:
                next_quote = db.query(Quote).order_by(Quote.id).first()
        else:
            # First time running, start with first quote
            next_quote = db.query(Quote).order_by(Quote.id).first()


if __name__ == "__main__":
    try:
        rotate_quote()
    except Exception as e:
        print(f"Error during rotation: {e}")
        sys.exit(1)
