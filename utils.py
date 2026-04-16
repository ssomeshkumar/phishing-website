"""
utils.py
Utility functions for URL validation, domain age, and common operations
"""

import re
from urllib.parse import urlparse
import tldextract
from datetime import datetime
import hashlib

def validate_url(url: str) -> bool:
    """
    Basic URL validation.
    Returns True if URL has a valid format.
    """
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain
        r'localhost|'  # localhost
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # IP
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, url) is not None

def extract_domain(url: str) -> str:
    """
    Extract the registered domain from a URL.
    Example: 'https://sub.example.co.uk/page' -> 'example.co.uk'
    """
    extracted = tldextract.extract(url)
    return f"{extracted.domain}.{extracted.suffix}"

def get_url_hash(url: str) -> str:
    """Generate a short hash for a URL (useful for caching)."""
    return hashlib.md5(url.encode()).hexdigest()[:8]

def format_timestamp(dt: datetime = None) -> str:
    """Return formatted timestamp for display."""
    if dt is None:
        dt = datetime.now()
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def calculate_risk_category(risk_score: float) -> tuple:
    """
    Convert numerical risk score to category label and color.
    Returns (category, color_hex)
    """
    if risk_score >= 70:
        return "High", "#f5576c"
    elif risk_score >= 40:
        return "Medium", "#f59f00"
    else:
        return "Low", "#51cf66"

def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """Safely divide two numbers, returning default if denominator is zero."""
    return numerator / denominator if denominator != 0 else default