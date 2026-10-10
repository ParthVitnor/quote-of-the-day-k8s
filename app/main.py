"""
FastAPI application for Quote of the Day.
Serves a single-page application showing a daily motivational quote.
"""
from fastapi import FastAPI, Depends, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from datetime import date

from app.database import get_db, init_db
from app.config import settings
from app.models import Quote, DailyQuote


# Initialize FastAPI app
app = FastAPI(
    title="Quote of the Day",
    description="A simple app that displays a daily motivational quote",
    version="1.0.0"
)

# Configure Jinja2 templates
templates = Jinja2Templates(directory=settings.TEMPLATES_DIR)


def get_daily_quote(db: Session) -> dict:
    """
    Get today's quote from the database.
    If no quote exists for today, runs rotation logic to set one.
    """
    today = date.today()
    
    # Query for today's quote
    daily_quote = db.query(DailyQuote).filter(DailyQuote.date == today).first()
    
    if not daily_quote:
        # No quote set for today, run rotation logic
        total_quotes = db.query(Quote).count()
        
        if total_quotes == 0:
            # No quotes in database, return placeholder
            return {
                "text": "The only way to do great work is to love what you do.",
                "author": "Steve Jobs"
            }
        
        # Get last used quote
        last_daily = db.query(DailyQuote).order_by(DailyQuote.date.desc()).first()
        
        if last_daily:
            # Sequential selection: get next quote
            last_quote_id = last_daily.quote_id
            next_quote = db.query(Quote).filter(Quote.id > last_quote_id).order_by(Quote.id).first()
            
            # If no next quote found, loop back to first
            if not next_quote:
                next_quote = db.query(Quote).order_by(Quote.id).first()
        else:
            # First time, start with first quote
            next_quote = db.query(Quote).order_by(Quote.id).first()
        
        # Insert new daily quote
        new_daily = DailyQuote(quote_id=next_quote.id, date=today)
        db.add(new_daily)
        db.commit()
        
        return {
            "text": next_quote.text,
            "author": next_quote.author
        }
    
    # Return the quote associated with today
    quote = db.query(Quote).filter(Quote.id == daily_quote.quote_id).first()
    return {
        "text": quote.text,
        "author": quote.author
    }


@app.on_event("startup")
async def startup_event():
    """Initialize database on application startup."""
    init_db()


@app.get("/health")
async def health_check():
    """
    Health check endpoint for Kubernetes liveness and readiness probes.
    Returns JSON with status.
    """
    return {"status": "ok"}


@app.get("/")
async def home(request: Request, db: Session = Depends(get_db)):
    """
    Homepage endpoint. Renders the Quote of the Day page.
    Gets today's quote from the database and passes it to the template.
    """
    quote_data = get_daily_quote(db)
    
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "quote": quote_data
        }
    )


@app.get("/api/quote/today")
async def get_todays_quote_api(db: Session = Depends(get_db)):
    """
    JSON API endpoint to get today's quote.
    Returns quote data as JSON for debugging or API consumption.
    """
    today = date.today()
    quote_data = get_daily_quote(db)
    quote_data["date"] = today.isoformat()
    
    return JSONResponse(content=quote_data)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True
    )
