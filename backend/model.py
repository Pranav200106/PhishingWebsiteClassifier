import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score

from parser import extract_url_features

data = pd.read_csv("../data/PhiUSIIL_Phishing_URL_Dataset.csv")

numeric_features = [
    "URLLength", "NoOfSubDomain", "NoOfObfuscatedChar", "ObfuscationRatio", 
    "NoOfQMarkInURL", "NoOfEqualsInURL", "NoOfOtherSpecialCharsInURL", "LetterRatioInURL"
]

binary_features = [
    'IsDomainIP', 'IsHTTPS'
]


preprocessor = ColumnTransformer(
    transformers=[
        ("num", StandardScaler(), numeric_features),
        #("bin", "passthrough", binary_features),
    ]
)

x = data.drop(columns=["label"])
y = data['label']

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, stratify=y, random_state=42)

clf = Pipeline(steps=[
    ("preprocess", preprocessor),
    ("classifier", LogisticRegression(max_iter=1000, C=0.5, class_weight="balanced"))
])


clf.fit(x_train, y_train)

y_preds = clf.predict(x_test)

accuracy = accuracy_score(y_test, y_preds)
clr = classification_report(y_test, y_preds)

url = input("Enter URL: ")
features = extract_url_features(url=url)
X = pd.DataFrame([features])

isPhishing = clf.predict(X)

output = {0: "Phishing URL", 1: "Legitamate URL"}

print(output[isPhishing[0]])
print(accuracy)
print(clr)
