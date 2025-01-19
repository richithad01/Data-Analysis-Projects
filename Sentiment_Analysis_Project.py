# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 21:39:20 2024

@author: richi
"""
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
from langdetect import detect
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer
from textblob import TextBlob 

data = pd.read_csv('chatgpt1.csv')

#creating function to create lang
x = data['Text'][0]
lang = detect(x)

def det(x):
    try:
        lang = detect(x)
    except:
        lang = 'Other'
    return lang

data['lang'] = data['Text'].apply(det)
data = data.loc[data['lang'] == 'en']
data = data.reset_index(drop=True)

#cleaning the data
data['Text'] = data['Text'].str.replace('https','')
data['Text'] = data['Text'].str.replace('http','')
data['Text'] = data['Text'].str.replace('t.co','')

#create a sentiment
def sentiment(text):
    sentiment = TextBlob(text).sentiment.polarity
    if sentiment > 0:
        return 'positive'
    elif sentiment < 0:
        return 'negative'
    else:
        return 'neutral'
data['Sentiment'] = data['Text'].apply(sentiment)

#generate wordcloud
comment_words = ''
stopwords = set(STOPWORDS)
for val in data.Text:
    val = str(val)
    tokens = val.split()
    comment_words = comment_words + " ".join(tokens) + " "
    
wordcloud = WordCloud(width=500,height=900,background_color='black',stopwords = stopwords,min_font_size=10).generate(comment_words)

plt.figure(figsize=(10,10))
plt.imshow(wordcloud)
plt.axis('off')
plt.tight_layout()
plt.show()

#create countplot for sentiment
sns.set_style('whitegrid')
plt.figure(figsize=(10,5))

sns.countplot(x='Sentiment',data=data)
plt.xlabel('Sentiment')
plt.ylabel('count of sentiments')
plt.show()