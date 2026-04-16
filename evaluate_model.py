"""
evaluate_model.py
Evaluate trained models and generate performance reports and visualizations
"""

import pickle
import pandas as pd
import numpy as np
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report, roc_curve, auc
)
import matplotlib.pyplot as plt
import seaborn as sns

def load_models():
    """Load all saved model artifacts."""
    with open('ensemble_model.pkl', 'rb') as f:
        ensemble = pickle.load(f)
    with open('decision_tree_model.pkl', 'rb') as f:
        dt = pickle.load(f)
    with open('naive_bayes_model.pkl', 'rb') as f:
        nb = pickle.load(f)
    with open('scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)
    with open('model_info.pkl', 'rb') as f:
        info = pickle.load(f)
    return ensemble, dt, nb, scaler, info

def evaluate_on_test_data():
    """Evaluate models on a test CSV file."""
    # Load dataset
    df = pd.read_csv('phishing_dataset.csv')
    feature_names = ['url_length', 'num_dots', 'has_https', 'domain_age_days',
                     'num_special_chars', 'uses_ip', 'num_suspicious_words',
                     'extension_type', 'url_depth', 'subdomain_count']

    X = df[feature_names].values
    y = df['label'].values

    # Split (same as training)
    from sklearn.model_selection import train_test_split
    _, X_test, _, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    # Load and scale
    ensemble, dt, nb, scaler, _ = load_models()
    X_test_scaled = scaler.transform(X_test)

    # Predictions
    dt_pred = dt.predict(X_test_scaled)
    nb_pred = nb.predict(X_test_scaled)
    ensemble_pred = ensemble.predict(X_test_scaled)

    print("=" * 60)
    print("MODEL EVALUATION REPORT")
    print("=" * 60)

    models = {'Decision Tree': dt_pred, 'Naive Bayes': nb_pred, 'Ensemble': ensemble_pred}
    for name, pred in models.items():
        print(f"\n{name}:")
        print(f"  Accuracy : {accuracy_score(y_test, pred):.4f}")
        print(f"  Precision: {precision_score(y_test, pred):.4f}")
        print(f"  Recall   : {recall_score(y_test, pred):.4f}")
        print(f"  F1-Score : {f1_score(y_test, pred):.4f}")

    # Confusion Matrix for Ensemble
    cm = confusion_matrix(y_test, ensemble_pred)
    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=['Normal', 'Phishing'],
                yticklabels=['Normal', 'Phishing'])
    plt.title('Ensemble Model - Confusion Matrix')
    plt.ylabel('Actual')
    plt.xlabel('Predicted')
    plt.tight_layout()
    plt.savefig('confusion_matrix.png', dpi=150)
    print("\n✅ Confusion matrix saved as 'confusion_matrix.png'")

    # ROC Curve
    ensemble_proba = ensemble.predict_proba(X_test_scaled)[:, 1]
    fpr, tpr, _ = roc_curve(y_test, ensemble_proba)
    roc_auc = auc(fpr, tpr)

    plt.figure(figsize=(6, 5))
    plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC (AUC = {roc_auc:.3f})')
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic')
    plt.legend(loc="lower right")
    plt.tight_layout()
    plt.savefig('roc_curve.png', dpi=150)
    print("✅ ROC curve saved as 'roc_curve.png'")

if __name__ == "__main__":
    evaluate_on_test_data()