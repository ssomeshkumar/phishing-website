import pandas as pd
import numpy as np
import random
import re

def generate_realistic_dataset(n_samples=10000):
    """
    Generate a realistic dataset with NO perfect correlations
    to prevent overfitting and create realistic ML challenge
    """
    np.random.seed(42)
    random.seed(42)
    
    data = []
    
    # Suspicious keywords and TLDs
    suspicious_keywords = [
        'secure', 'account', 'update', 'verify', 'login', 'signin', 'banking',
        'confirm', 'paypal', 'security', 'alert', 'password', 'credential',
        'limited', 'suspend', 'unlock', 'authenticate', 'validation'
    ]
    
    suspicious_tlds = ['.tk', '.ml', '.ga', '.cf', '.xyz', '.top', '.work', '.gq', '.loan', '.win']
    normal_tlds = ['.com', '.org', '.net', '.edu', '.gov', '.io', '.co', '.info', '.biz']
    
    legitimate_domains = [
        'google.com', 'facebook.com', 'youtube.com', 'amazon.com', 'wikipedia.org',
        'twitter.com', 'instagram.com', 'linkedin.com', 'netflix.com', 'microsoft.com',
        'apple.com', 'github.com', 'stackoverflow.com', 'reddit.com', 'spotify.com',
        'dropbox.com', 'adobe.com', 'salesforce.com', 'oracle.com', 'ibm.com',
        'nytimes.com', 'cnn.com', 'bbc.com', 'medium.com', 'quora.com'
    ]
    
    for i in range(n_samples):
        # Decide if phishing (35%) or legitimate (65%) - imbalanced realistic
        is_phishing = random.random() < 0.35
        
        if is_phishing:
            # PHISHING URL GENERATION
            keyword1 = random.choice(suspicious_keywords)
            keyword2 = random.choice(suspicious_keywords)
            
            # 70% chance of suspicious TLD, 30% normal TLD (to make it challenging)
            if random.random() < 0.7:
                tld = random.choice(suspicious_tlds)
                extension_type = 1
            else:
                tld = random.choice(normal_tlds)
                extension_type = 0
            
            patterns = [
                f"http://{keyword1}-{keyword2}-verify{tld}/login",
                f"http://{keyword1}.{keyword2}-secure{tld}/account",
                f"https://{keyword1}verification{tld}/confirm",
                f"http://secure-{keyword1}-{keyword2}{tld}/signin",
                f"http://verify-{keyword1}-account{tld}/security",
                f"http://www.{keyword1}-secure{tld}/update",
                f"https://{keyword1}.{keyword2}{tld}/login/verify",
                f"http://account-{keyword1}{tld}/password-reset"
            ]
            url = random.choice(patterns)
            
            # Add random query params sometimes
            if random.random() < 0.4:
                url += f"?id={random.randint(1000, 9999)}&token={random.randint(10000, 99999)}"
            
            # Calculate features with realistic variations
            url_length = len(url) + np.random.randint(-15, 25)
            num_dots = url.count('.') + np.random.randint(-1, 3)
            
            # Phishing sites sometimes use HTTPS (30% chance)
            has_https = 1 if url.startswith('https') else random.choice([0, 1, 0, 0])
            
            # Domain age (newer for phishing, but with overlap)
            domain_age_days = int(np.random.exponential(120)) + 1
            domain_age_days = min(365, domain_age_days)
            
            num_special_chars = len(re.findall(r'[-/_?=&@#%]', url)) + np.random.randint(-2, 4)
            uses_ip = 1 if random.random() < 0.05 else 0  # 5% use IP
            
            # Suspicious words count (with noise)
            num_suspicious_words = sum(1 for word in suspicious_keywords if word in url.lower())
            num_suspicious_words = max(0, num_suspicious_words + np.random.randint(-1, 2))
            
            url_depth = max(1, url.count('/') - 2 + np.random.randint(-1, 3))
            subdomain_count = max(0, url.count('.') - 1 + np.random.randint(-1, 2))
            label = 1
            
        else:
            # LEGITIMATE URL GENERATION
            domain = random.choice(legitimate_domains)
            paths = ['', '/about', '/contact', '/products', '/services', '/blog', 
                    '/news', '/help', '/support', '/faq', '/terms', '/privacy',
                    '/careers', '/team', '/portfolio', '/docs', '/api']
            path = random.choice(paths)
            
            # 85% HTTPS, 15% HTTP
            protocol = 'https' if random.random() < 0.85 else 'http'
            # 60% www, 40% no www
            www = 'www.' if random.random() < 0.6 else ''
            
            url = f"{protocol}://{www}{domain}{path}"
            
            if random.random() < 0.3:
                url += f"?page={random.randint(1, 10)}&view={random.choice(['grid', 'list'])}"
            
            # Calculate features
            url_length = len(url) + np.random.randint(-10, 20)
            num_dots = url.count('.') + np.random.randint(-1, 2)
            has_https = 1 if protocol == 'https' else 0
            
            # Domain age (older for legitimate, but with overlap)
            domain_age_days = int(np.random.gamma(2, 400)) + 50
            domain_age_days = max(30, min(3000, domain_age_days))
            
            num_special_chars = len(re.findall(r'[-/_?=&@#%]', url)) + np.random.randint(-2, 3)
            uses_ip = 0
            
            # Legitimate sites occasionally have suspicious words (e.g., "secure login")
            num_suspicious_words = 0
            if random.random() < 0.1:  # 10% chance
                num_suspicious_words = 1
            
            # 85% normal extension, 15% suspicious (to make it challenging)
            extension_type = 0 if random.random() < 0.85 else 1
            
            url_depth = max(1, url.count('/') - 2 + np.random.randint(-1, 2))
            subdomain_count = max(0, url.count('.') - 1 + np.random.randint(-1, 1))
            label = 0
        
        # Ensure valid ranges
        url_length = max(20, min(400, int(url_length)))
        num_dots = max(1, min(12, int(num_dots)))
        num_special_chars = max(0, min(20, int(num_special_chars)))
        domain_age_days = max(1, min(5000, int(domain_age_days)))
        num_suspicious_words = max(0, min(6, int(num_suspicious_words)))
        url_depth = max(1, min(10, int(url_depth)))
        subdomain_count = max(0, min(5, int(subdomain_count)))
        
        data.append({
            'url': url,
            'url_length': url_length,
            'num_dots': num_dots,
            'has_https': has_https,
            'domain_age_days': domain_age_days,
            'num_special_chars': num_special_chars,
            'uses_ip': uses_ip,
            'num_suspicious_words': num_suspicious_words,
            'extension_type': extension_type,
            'url_depth': url_depth,
            'subdomain_count': subdomain_count,
            'label': label
        })
    
    df = pd.DataFrame(data)
    
    # Add realistic edge cases
    edge_cases = [
        # Legitimate but look suspicious
        ["https://secure.login.microsoftonline.com/oauth2/authorize", 58, 3, 1, 850, 4, 0, 1, 0, 3, 2, 0],
        ["https://accounts.google.com/signin/v2/security", 48, 2, 1, 1200, 3, 0, 1, 0, 4, 1, 0],
        ["https://www.paypal.com/signin?country.x=US", 41, 2, 1, 2500, 4, 0, 1, 0, 1, 1, 0],
        ["https://verify.apple.com/account/login", 38, 2, 1, 1800, 2, 0, 1, 0, 3, 1, 0],
        
        # Phishing that look legitimate
        ["https://paypal.com.verify.tk/login", 34, 2, 1, 15, 1, 0, 2, 1, 2, 2, 1],
        ["http://accounts.google.com.secure.ml/verify", 45, 3, 0, 8, 2, 0, 2, 1, 2, 3, 1],
        ["https://appleid.apple.com.xyz/account/update", 44, 3, 1, 25, 2, 0, 2, 1, 3, 3, 1],
        ["http://microsoft.com.security-alert.ga/login", 46, 3, 0, 12, 2, 0, 3, 1, 2, 3, 1],
    ]
    
    for case in edge_cases:
        df.loc[len(df)] = case
    
    # Shuffle dataset
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)
    
    return df

if __name__ == "__main__":
    print("🔄 Generating REALISTIC phishing dataset...")
    print("="*60)
    
    df = generate_realistic_dataset(10000)
    
    # Save dataset
    df.to_csv('phishing_dataset.csv', index=False)
    
    print(f"✅ Dataset saved successfully!")
    print(f"📊 Total samples: {len(df):,}")
    print(f"🎯 Phishing: {df['label'].sum():,} ({df['label'].mean()*100:.1f}%)")
    print(f"✅ Normal: {len(df)-df['label'].sum():,} ({(1-df['label'].mean())*100:.1f}%)")
    
    print("\n📈 Feature Correlations with Label:")
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        if col not in ['label']:
            corr = df[col].corr(df['label'])
            bar = "█" * int(abs(corr) * 50)
            print(f"  {col:20s}: {corr:+.3f} {bar}")
    
    print("\n🎯 Expected Model Performance (realistic):")
    print("  • Target Accuracy: 85-92% (not 100%)")
    print("  • This dataset prevents overfitting")
    print("  • Models will generalize well to new URLs")
    
    print("\n📋 Sample URLs:")
    for i in range(3):
        row = df[df['label'] == 1].iloc[i]
        print(f"\n  ⚠️ PHISHING: {row['url'][:60]}...")
        print(f"     Length: {row['url_length']}, HTTPS: {row['has_https']}, Age: {row['domain_age_days']}d")
    
    for i in range(3):
        row = df[df['label'] == 0].iloc[i]
        print(f"\n  ✅ NORMAL: {row['url'][:60]}...")
        print(f"     Length: {row['url_length']}, HTTPS: {row['has_https']}, Age: {row['domain_age_days']}d")