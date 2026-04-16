"""
history_manager.py
Manage prediction history with optional JSON persistence
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional
from config import HISTORY_FILE, MAX_HISTORY_ITEMS

class HistoryManager:
    def __init__(self, max_items: int = MAX_HISTORY_ITEMS, persist: bool = True):
        self.max_items = max_items
        self.persist = persist
        self.history: List[Dict] = []
        if persist:
            self.load()

    def add_entry(self, url: str, prediction: int, confidence: float,
                  risk_score: float, features: Dict, model_votes: Dict) -> None:
        """Add a new prediction to history."""
        entry = {
            'timestamp': datetime.now().isoformat(),
            'url': url,
            'prediction': 'PHISHING' if prediction == 1 else 'NORMAL',
            'prediction_bool': prediction,
            'confidence': round(confidence, 4),
            'risk_score': round(risk_score, 2),
            'features': features,
            'model_votes': model_votes
        }
        self.history.append(entry)
        # Keep only last max_items
        if len(self.history) > self.max_items:
            self.history = self.history[-self.max_items:]
        if self.persist:
            self.save()

    def get_history(self, limit: Optional[int] = None) -> List[Dict]:
        """Return recent history entries (most recent first)."""
        if limit:
            return list(reversed(self.history[-limit:]))
        return list(reversed(self.history))

    def clear(self) -> None:
        """Clear all history."""
        self.history = []
        if self.persist and os.path.exists(HISTORY_FILE):
            os.remove(HISTORY_FILE)

    def get_statistics(self) -> Dict:
        """Calculate summary statistics from history."""
        total = len(self.history)
        if total == 0:
            return {'total_scans': 0, 'phishing_count': 0, 'normal_count': 0,
                    'phishing_rate': 0, 'avg_confidence': 0, 'avg_risk': 0}

        phishing_count = sum(1 for e in self.history if e['prediction_bool'] == 1)
        normal_count = total - phishing_count
        avg_confidence = sum(e['confidence'] for e in self.history) / total
        avg_risk = sum(e['risk_score'] for e in self.history) / total

        return {
            'total_scans': total,
            'phishing_count': phishing_count,
            'normal_count': normal_count,
            'phishing_rate': round(phishing_count / total * 100, 1),
            'avg_confidence': round(avg_confidence, 3),
            'avg_risk': round(avg_risk, 2)
        }

    def save(self) -> None:
        """Save history to JSON file."""
        try:
            with open(HISTORY_FILE, 'w') as f:
                json.dump(self.history, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save history: {e}")

    def load(self) -> None:
        """Load history from JSON file."""
        if not os.path.exists(HISTORY_FILE):
            return
        try:
            with open(HISTORY_FILE, 'r') as f:
                self.history = json.load(f)
            # Trim if necessary
            if len(self.history) > self.max_items:
                self.history = self.history[-self.max_items:]
        except Exception as e:
            print(f"Warning: Could not load history: {e}")

    def export_csv(self) -> str:
        """Export history as CSV string."""
        if not self.history:
            return "timestamp,url,prediction,confidence,risk_score"
        rows = ["timestamp,url,prediction,confidence,risk_score"]
        for entry in self.history:
            rows.append(f"{entry['timestamp']},{entry['url']},{entry['prediction']},"
                       f"{entry['confidence']},{entry['risk_score']}")
        return "\n".join(rows)