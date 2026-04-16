"""
test_detector.py
Unit tests for the phishing detection system
"""

import unittest
import sys
import os
import numpy as np
from feature_extractor import extract_features, get_feature_names
from utils import validate_url, extract_domain, calculate_risk_category

class TestFeatureExtractor(unittest.TestCase):

    def test_extract_features_legitimate(self):
        url = "https://www.google.com/search?q=test"
        features = extract_features(url)

        self.assertEqual(features['has_https'], 1)
        self.assertGreater(features['url_length'], 20)
        self.assertGreaterEqual(features['num_dots'], 2)
        self.assertEqual(features['uses_ip'], 0)
        self.assertEqual(features['extension_type'], 0)
        self.assertLess(features['num_suspicious_words'], 2)

    def test_extract_features_phishing(self):
        url = "http://secure-login-verify.tk/update?account=123"
        features = extract_features(url)

        self.assertEqual(features['has_https'], 0)
        self.assertGreater(features['num_suspicious_words'], 0)
        self.assertEqual(features['extension_type'], 1)
        self.assertLess(features['domain_age_days'], 365)

    def test_feature_names_order(self):
        names = get_feature_names()
        expected = ['url_length', 'num_dots', 'has_https', 'domain_age_days',
                    'num_special_chars', 'uses_ip', 'num_suspicious_words',
                    'extension_type', 'url_depth', 'subdomain_count']
        self.assertEqual(names, expected)

    def test_ip_address_detection(self):
        url = "http://192.168.1.1/admin"
        features = extract_features(url)
        self.assertEqual(features['uses_ip'], 1)

class TestUtils(unittest.TestCase):

    def test_validate_url(self):
        self.assertTrue(validate_url("https://example.com"))
        self.assertTrue(validate_url("http://sub.domain.co.uk/path"))
        self.assertFalse(validate_url("not-a-url"))
        self.assertFalse(validate_url("ftp://example.com"))  # Only http/https

    def test_extract_domain(self):
        self.assertEqual(extract_domain("https://mail.google.com/inbox"), "google.com")
        self.assertEqual(extract_domain("http://test.example.co.uk/page"), "example.co.uk")

    def test_risk_category(self):
        cat, color = calculate_risk_category(85)
        self.assertEqual(cat, "High")
        cat, _ = calculate_risk_category(50)
        self.assertEqual(cat, "Medium")
        cat, _ = calculate_risk_category(20)
        self.assertEqual(cat, "Low")

class TestModelLoading(unittest.TestCase):

    @unittest.skipIf(not os.path.exists('ensemble_model.pkl'),
                     "Model files not found. Run training first.")
    def test_model_files_exist(self):
        required = ['ensemble_model.pkl', 'decision_tree_model.pkl',
                    'naive_bayes_model.pkl', 'scaler.pkl']
        for f in required:
            self.assertTrue(os.path.exists(f), f"Missing {f}")

    @unittest.skipIf(not os.path.exists('ensemble_model.pkl'),
                     "Model files not found.")
    def test_model_prediction_shape(self):
        import pickle
        with open('ensemble_model.pkl', 'rb') as f:
            model = pickle.load(f)
        # Create dummy feature vector (10 features)
        dummy = np.random.randn(1, 10)
        pred = model.predict(dummy)
        self.assertEqual(pred.shape, (1,))

if __name__ == '__main__':
    # Run tests
    unittest.main(verbosity=2)