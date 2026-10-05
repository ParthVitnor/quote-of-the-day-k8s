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
    # TODO: Implement get_daily_quote logic
    # For now, return a placeholder
    quote_data = {
        "text": "The only way to do great work is to love what you do.",
        "author": "Steve Jobs"
    }
    
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
    # TODO: Implement get_daily_quote logic
    today = date.today()
    
    quote_data = {
        "text": "The only way to do great work is to love what you do.",
        "author": "Steve Jobs",
        "date": today.isoformat()
    }
    
    return JSONResponse(content=quote_data)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True
    )
