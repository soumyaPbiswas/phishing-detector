Phishing URL Detection System: 

This project is a machine learning powered phishing detection web app.
It analyzes a URL using a hybrid approach that combines:

URL lexical analysis
HTTP response properties
HTML structure inspection (forms, scripts, redirects, frames)
Lightweight behavioral signals
The model predicts whether a given URL is likely legitimate or a phishing attempt.

Features-
Web interface built with Flask
Machine learning model trained on a hybrid dataset
Real-time URL scanning and feature extraction
Confidence scoring
Works on unknown and previously unseen URLs

How It Works-
A user submits a URL through the interface.
The application extracts features from the URL such as:
Length, subdomains, special characters
Security indicators (HTTPS, redirects)
Presence of forms and password fields
The extracted features are passed to a trained machine learning model.
The model outputs a classification: Safe or Phishing along with a confidence percentage.

Tech Stack-
Component	Technology
Backend	Python, Flask
ML Stack	Scikit-learn, Joblib
Parsing	BeautifulSoup4, Requests
Feature Extraction	tldextract, custom rules
Frontend	TailwindCSS + HTML
