import pandas as pd
import spacy
from nltk.sentiment import SentimentIntensityAnalyzer

nlp = spacy.load("en_core_web_sm")
sia = SentimentIntensityAnalyzer()

# Load data
emails = pd.read_csv("data/emails.csv")

# Preprocess
def analyze_sentiment(text):
    return sia.polarity_scores(text)['compound']

def named_entities(text):
    doc = nlp(text)
    return [ent.text for ent in doc.ents]

emails["sentiment"] = emails["message"].apply(analyze_sentiment)
emails["entities"] = emails["message"].apply(named_entities)

emails.to_csv("data/emails_processed.csv", index=False)
print(emails.head())
