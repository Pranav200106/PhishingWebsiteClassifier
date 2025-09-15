from urllib.parse import urlparse
import re
from collections import Counter

def extract_url_features(url):
    features = {}

    # --- Text features ---
    domain = urlparse(url).netloc

    # --- Numeric features ---
    features['URLLength'] = len(url)
    features['NoOfSubDomain'] = max(len(domain.split('.')) - 1, 0)

    letters = sum(c.isalpha() for c in url)
    features['LetterRatioInURL'] = letters / len(url) if len(url) > 0 else 0


    features['NoOfEqualsInURL'] = url.count('=')
    features['NoOfQMarkInURL'] = url.count('?')

    special_chars = re.findall(r'[^a-zA-Z0-9=&]', url)
    features['NoOfOtherSpecialCharsInURL'] = len(special_chars)

    obfuscated_chars = re.findall(r'[@\-_~]', url)
    features['NoOfObfuscatedChar'] = len(obfuscated_chars)
    features['ObfuscationRatio'] = len(obfuscated_chars) / len(url) if len(url) > 0 else 0

    features['IsDomainIP'] = 1 if re.match(r'^\d{1,3}(\.\d{1,3}){3}$', domain) else 0
    features['IsHTTPS'] = 1 if url.startswith('https') else 0

    return features
