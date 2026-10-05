"""
SQLAlchemy models for Quote of the Day application.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Date, ForeignKey, Text
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Quote(Base):
    """Model for storing all available quotes."""
    
    __tablename__ = "quotes"
    
    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    author = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationship to daily quotes
    daily_quotes = relationship("DailyQuote", back_populates="quote")
    
    def __repr__(self):
        return f"<Quote(id={self.id}, author='{self.author}')>"


class DailyQuote(Base):
    """Model for tracking which quote is shown each day."""
    
    __tablename__ = "daily_quote"
    
    id = Column(Integer, primary_key=True, index=True)
    quote_id = Column(Integer, ForeignKey("quotes.id"), nullable=False)
    date = Column(Date, unique=True, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationship to quote
    quote = relationship("Quote", back_populates="daily_quotes")
    
    def __repr__(self):
        return f"<DailyQuote(date={self.date}, quote_id={self.quote_id})>"
