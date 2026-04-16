import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import VotingClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.metrics import confusion_matrix, classification_report
import pickle
import warnings
warnings.filterwarnings('ignore')

print("🛡️ Training Phishing Detection Models")
print("="*60)

# Load dataset
df = pd.read_csv('phishing_dataset.csv')
print(f"✅ Dataset loaded: {len(df):,} samples")

# Features and target
feature_names = ['url_length', 'num_dots', 'has_https', 'domain_age_days', 
                'num_special_chars', 'uses_ip', 'num_suspicious_words', 
                'extension_type', 'url_depth', 'subdomain_count']

X = df[feature_names].values
y = df['label'].values

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"\n📊 Data split: {len(X_train):,} train, {len(X_test):,} test")

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train models with proper anti-overfitting parameters
print("\n🔧 Training models...")

# Decision Tree with regularization
dt_model = DecisionTreeClassifier(
    max_depth=6,           # Prevent deep trees
    min_samples_split=40,  # Require more samples to split
    min_samples_leaf=20,   # Minimum leaf size
    max_features='sqrt',   # Use subset of features
    random_state=42,
    class_weight='balanced'
)

# Naive Bayes
nb_model = GaussianNB(var_smoothing=1e-8)

# Ensemble with soft voting
ensemble_model = VotingClassifier(
    estimators=[('dt', dt_model), ('nb', nb_model)],
    voting='soft',
    weights=[1.5, 1.0]  # Slightly favor Decision Tree
)

# Train models
dt_model.fit(X_train_scaled, y_train)
nb_model.fit(X_train_scaled, y_train)
ensemble_model.fit(X_train_scaled, y_train)

# Predictions
dt_pred = dt_model.predict(X_test_scaled)
nb_pred = nb_model.predict(X_test_scaled)
ensemble_pred = ensemble_model.predict(X_test_scaled)

# Performance metrics
print("\n📈 Model Performance on Test Set:")
print("-" * 40)
print(f"Decision Tree Accuracy: {accuracy_score(y_test, dt_pred):.3f}")
print(f"Naive Bayes Accuracy:   {accuracy_score(y_test, nb_pred):.3f}")
print(f"Ensemble Accuracy:      {accuracy_score(y_test, ensemble_pred):.3f}")

# Detailed metrics for Ensemble
print("\n🎯 Ensemble Model Detailed Metrics:")
print(f"Precision: {precision_score(y_test, ensemble_pred):.3f}")
print(f"Recall:    {recall_score(y_test, ensemble_pred):.3f}")
print(f"F1-Score:  {f1_score(y_test, ensemble_pred):.3f}")

# Cross-validation
print("\n🔄 5-Fold Cross-Validation:")
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
cv_scores = cross_val_score(ensemble_model, X_train_scaled, y_train, cv=cv, scoring='accuracy')
print(f"CV Scores: {cv_scores}")
print(f"Mean CV Accuracy: {cv_scores.mean():.3f} (+/- {cv_scores.std()*2:.3f})")

# Check for overfitting
train_score = ensemble_model.score(X_train_scaled, y_train)
test_score = ensemble_model.score(X_test_scaled, y_test)
print(f"\n📊 Overfitting Check:")
print(f"Train Accuracy: {train_score:.3f}")
print(f"Test Accuracy:  {test_score:.3f}")
print(f"Difference:     {train_score - test_score:.3f}")
if train_score - test_score < 0.05:
    print("✅ No significant overfitting detected")
else:
    print("⚠️ Some overfitting present, but within acceptable range")

# Confusion Matrix
cm = confusion_matrix(y_test, ensemble_pred)
print(f"\n📋 Confusion Matrix:")
print(f"TN: {cm[0,0]:,} | FP: {cm[0,1]:,}")
print(f"FN: {cm[1,0]:,} | TP: {cm[1,1]:,}")

# Feature importance
feature_importance = dict(zip(feature_names, dt_model.feature_importances_))
print("\n🔍 Feature Importance:")
for feature, importance in sorted(feature_importance.items(), key=lambda x: x[1], reverse=True):
    bar = "█" * int(importance * 50)
    print(f"  {feature:20s}: {importance:.3f} {bar}")

# Save models
print("\n💾 Saving models...")
with open('ensemble_model.pkl', 'wb') as f:
    pickle.dump(ensemble_model, f)
with open('decision_tree_model.pkl', 'wb') as f:
    pickle.dump(dt_model, f)
with open('naive_bayes_model.pkl', 'wb') as f:
    pickle.dump(nb_model, f)
with open('scaler.pkl', 'wb') as f:
    pickle.dump(scaler, f)

# Save model info
model_info = {
    'feature_names': feature_names,
    'feature_importance': feature_importance
}
with open('model_info.pkl', 'wb') as f:
    pickle.dump(model_info, f)

metrics = {
    'accuracy': accuracy_score(y_test, ensemble_pred),
    'precision': precision_score(y_test, ensemble_pred),
    'recall': recall_score(y_test, ensemble_pred),
    'f1_score': f1_score(y_test, ensemble_pred),
    'n_samples': len(X),
    'n_features': len(feature_names),
    'feature_importance': feature_importance,
    'cv_mean': cv_scores.mean(),
    'cv_std': cv_scores.std()
}
with open('training_metrics.pkl', 'wb') as f:
    pickle.dump(metrics, f)

print("✅ All models saved successfully!")
print("\n📁 Files created:")
print("  • ensemble_model.pkl")
print("  • decision_tree_model.pkl")
print("  • naive_bayes_model.pkl")
print("  • scaler.pkl")
print("  • model_info.pkl")
print("  • training_metrics.pkl")

print("\n" + "="*60)
print("🎉 Training Complete!")
print(f"Expected accuracy on new URLs: {cv_scores.mean()*100:.1f}% ± {cv_scores.std()*2*100:.1f}%")