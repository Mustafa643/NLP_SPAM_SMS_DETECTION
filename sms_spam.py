
## IMPORT  LIBRARIES


!pip install chardet

import os

import chardet  ##ENCODING LIBRARY
import pandas as pd
import numpy as np
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
nltk.download('punkt')
nltk.download('stopwords')



import spacy
nlp = spacy.load('en_core_web_sm')
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from google.colab import drive

import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

"""## MOUNT DRIVE AND LOAD DATA"""

drive.mount('/content/drive')
os.listdir('/content/drive/My Drive/')

"""## DETECT ENCODING ON THE DOWNLOADED CSV FILE"""

rawdata = open('/content/drive/My Drive/SMS_Spam.csv', 'rb').read()
result = chardet.detect(rawdata)
encoding = result['encoding']
print(f"Detected encoding: {encoding}")

data = pd.read_csv('/content/drive/My Drive/SMS_Spam.csv', encoding='Windows-1252')

"""## READ FROM DATA

"""

data.head()

"""## Get information about the DataFrame"""

data.info()

"""## Summary statistics"""

data.describe()

"""## WORD TOKENIZATION"""

texts = data['v2'].tolist()  #v2 is column with Message
labels = data['v1'].tolist()   # v1 is column with Label (ham or spam)
print(texts[:20])  # First 20 entries to Verify

"""## TOKENIZE FIRST 20 ENTRIES"""

tokenized_texts_nltk = [word_tokenize(text) for text in texts]
print(tokenized_texts_nltk[:20])

"""## INITIALIZE STEMMER & FUNCTION TO PERFORM STEEMER"""

stemmer = PorterStemmer()
def stem_text(text):
    tokens = word_tokenize(text)
    return ' '.join([stemmer.stem(token) for token in tokens])

"""## APPLY STEMMING TO EACH TEXT ENTRY"""

texts = data['v2'].tolist()
labels = data['v1'].tolist()
print(texts[:20])

stemmed_texts = [stem_text(text) for text in texts]
print("Stemmed texts:", stemmed_texts[:20])

"""## LEMMATIZATION USING SPACY"""

def lemmatize_text(text):
    doc = nlp(text)
    return ' '.join([token.lemma_ for token in doc])

texts = data['v2'].tolist()
labels = data['v1'].tolist()
print(texts[:20])

lemmatized_texts = [lemmatize_text(text) for text in texts]
print("Lemmatized texts:", lemmatized_texts[:20])

## STOP WORD REMOVAL

stop_words = set(stopwords.words('english'))

"""## TOKENIZE AND REMOVE ENGLISH WORD"""

def tokenize_and_remove_stopwords(text):
    tokens = word_tokenize(text)
    filtered_tokens = [token for token in tokens if token.lower() not in stop_words]
    return filtered_tokens
print(texts[:20])
tokenized_texts = [tokenize_and_remove_stopwords(text) for text in texts]
print("Tokenized texts without stopwords:", tokenized_texts[:20])

"""#PERFORM STEEMING ON TOKENS"""

stemmer = PorterStemmer()
def stem_tokens(tokens):
    return [stemmer.stem(token) for token in tokens]
print(texts[:20])
stemmed_texts = [' '.join(stem_tokens(tokens)) for tokens in tokenized_texts]
print("Stemmed texts:", stemmed_texts[:5])

"""## PERFORM LEMMATIZATIONS ONM TOKENS"""

def lemmatize_text(text):
    doc = nlp(text)
    return ' '.join([token.lemma_ for token in doc])

lemmatized_texts = [lemmatize_text(' '.join(tokens)) for tokens in tokenized_texts]
print("Lemmatized texts:", lemmatized_texts[:20])

"""##PART OF SPEECH TAGGING ON TOKENIZED TEXTS (using spacy)"""

def pos_tag_spacy(text):
    doc = nlp(text)
    return [(token.text, token.pos_) for token in doc]

pos_tagged_texts_spacy = [pos_tag_spacy(' '.join(tokens)) for tokens in tokenized_texts]
print("POS tagged texts using spacy:", pos_tagged_texts_spacy[:20])

"""## OUTPUT PROCESSED TEXT"""

data['processed_text'] = stemmed_texts  # Use stemmed_texts or lemmatized_texts

data.head()

output_file_path = '/content/drive/My Drive/processed_spam.csv'
data.to_csv(output_file_path, index=False)
print(f'Processed data saved to {output_file_path}')
