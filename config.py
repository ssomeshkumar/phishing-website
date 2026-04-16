"""
config.py
Central configuration for the phishing detection system
"""

# Model file paths
MODEL_PATHS = {
    'ensemble': 'ensemble_model.pkl',
    'decision_tree': 'decision_tree_model.pkl',
    'naive_bayes': 'naive_bayes_model.pkl',
    'scaler': 'scaler.pkl',
    'model_info': 'model_info.pkl',
    'metrics': 'training_metrics.pkl'
}

# Dataset path
DATASET_PATH = 'phishing_dataset.csv'

# History file (optional persistence)
HISTORY_FILE = 'prediction_history.json'

# Feature names (must match training order)
FEATURE_NAMES = [
    'url_length', 'num_dots', 'has_https', 'domain_age_days',
    'num_special_chars', 'uses_ip', 'num_suspicious_words',
    'extension_type', 'url_depth', 'subdomain_count'
]

# Suspicious patterns
SUSPICIOUS_KEYWORDS = [
    'secure', 'account', 'update', 'verify', 'login', 'signin', 'banking',
    'confirm', 'paypal', 'security', 'alert', 'password', 'credential',
    'limited', 'suspend', 'unlock', 'authenticate', 'validation'
]

SUSPICIOUS_TLDS = ['.tk', '.ml', '.ga', '.cf', '.xyz', '.top', '.work', '.gq', '.loan', '.win']

# Risk thresholds
RISK_HIGH_THRESHOLD = 70
RISK_MEDIUM_THRESHOLD = 40

# Application settings
APP_NAME = "PhishGuard AI"
APP_VERSION = "1.0.0"
MAX_HISTORY_ITEMS = 50

# Color scheme
COLORS = {
    'primary': '#667eea',
    'secondary': '#764ba2',
    'danger': '#f5576c',
    'success': '#4facfe',
    'warning': '#f59f00',
    'info': '#00f2fe'
}