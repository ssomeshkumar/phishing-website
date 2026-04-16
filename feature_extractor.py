"""
feature_extractor.py
Extracts numerical features from a raw URL string for model input
"""

import re
from urllib.parse import urlparse

# Suspicious patterns
SUSPICIOUS_KEYWORDS = [
    'secure', 'account', 'update', 'verify', 'login', 'signin', 'banking',
    'confirm', 'paypal', 'security', 'alert', 'password', 'credential',
    'limited', 'suspend', 'unlock', 'authenticate', 'validation'
]

SUSPICIOUS_TLDS = ['.tk', '.ml', '.ga', '.cf', '.xyz', '.top', '.work', '.gq', '.loan', '.win']

def extract_features(url: str) -> dict:
    """
    Extract all required features from a URL.
    Returns a dictionary with feature names as keys.
    """
    parsed = urlparse(url)
    features = {}

    # Basic length and count features
    features['url_length'] = len(url)
    features['num_dots'] = url.count('.')
    features['has_https'] = 1 if parsed.scheme == 'https' else 0

    # Special characters
    special_chars = len(re.findall(r'[-/_?=&@#%]', url))
    features['num_special_chars'] = special_chars

    # IP address usage
    features['uses_ip'] = 1 if re.search(r'\d+\.\d+\.\d+\.\d+', url) else 0

    # Suspicious words
    lower_url = url.lower()
    suspicious_count = sum(1 for word in SUSPICIOUS_KEYWORDS if word in lower_url)
    features['num_suspicious_words'] = suspicious_count

    # Suspicious TLD
    features['extension_type'] = 1 if any(tld in url for tld in SUSPICIOUS_TLDS) else 0

    # URL depth (number of path segments)
    path = parsed.path
    depth = len([seg for seg in path.split('/') if seg]) if path else 1
    features['url_depth'] = depth

    # Subdomain count
    netloc = parsed.netloc
    subdomain_count = netloc.count('.') - 1 if netloc else 0
    features['subdomain_count'] = max(0, subdomain_count)

    # Domain age estimation (simplified, use WHOIS in production)
    features['domain_age_days'] = estimate_domain_age(url)

    return features

def estimate_domain_age(url: str) -> int:
    """
    Estimate domain age based on heuristics.
    In production, replace with actual WHOIS lookup.
    """
    try:
        parsed = urlparse(url)
        domain = parsed.netloc.split(':')[0]
        # Pseudo-age based on domain string hash (for demo consistency)
        domain_hash = sum(ord(c) for c in domain)
        age = (domain_hash % 1000) + 100

        # Suspicious TLDs tend to be newer
        if any(tld in domain for tld in SUSPICIOUS_TLDS):
            age = min(age, 90)
        return age
    except:
        return 365  # Default

def get_feature_names() -> list:
    """Return list of feature names in correct order."""
    return ['url_length', 'num_dots', 'has_https', 'domain_age_days',
            'num_special_chars', 'uses_ip', 'num_suspicious_words',
            'extension_type', 'url_depth', 'subdomain_count']

def features_to_array(features: dict, feature_names: list = None) -> list:
    """Convert feature dict to ordered list for model input."""
    if feature_names is None:
        feature_names = get_feature_names()
    return [features[name] for name in feature_names]