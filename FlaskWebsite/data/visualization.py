
import pandas as pd
from keybert import KeyBERT
import re
from bertopic import BERTopic
import os
# from python_settings import settings

# import nltk
# from nltk.tokenize import word_tokenize
# from nltk.stem import WordNetLemmatizer
import spacy
from spacy.lang.fr.stop_words import STOP_WORDS as fr_stop
nlp = spacy.load('fr_core_news_md')
# nltk.download('wordnet')
# nltk.download('punkt')
stopwords = list(fr_stop)
kw_model = KeyBERT()


def get_visualization(dfTweeets):
    APP_ROOT = os.path.dirname(os.path.abspath(__file__))   # refers to application_top
    APP_STATIC = os.path.join(APP_ROOT, '../static')
    file = os.path.join(APP_STATIC, "ZemmourEric-2022-02-02 01_25_27.355764.csv")
    # df = pd.read_csv(file, encoding = 'UTF-8')
    
    df = dfTweeets
    df['preprocessed']= df['tweet_text'].astype(str).apply(preprocessing_final)
    df['keywords']= df['preprocessed'].apply(keyword_extraction)

    df.time = pd.to_datetime(df['time'], dayfirst=True)
    timestamps = df.time.astype(str).to_list()
    tweets = df.keywords.astype(str).to_list()

    topic_model = BERTopic(language="French", n_gram_range=(1, 3))
    topics, probs = topic_model.fit_transform(tweets)

    topics_over_time = topic_model.topics_over_time(tweets, topics, timestamps, 
                                                global_tuning=False, 
                                                evolution_tuning=True,
                                                nr_bins=20)
    
    file_name = "file123.html"
    topics_over_time.write_html(file_name)

    # topic_model.visualize_topics_over_time(topics_over_time, top_n_topics=6)
    # topics_df = topics_over_time[['Topic','Frequency','Name','Timestamp']]
    # topics_df.to_csv(file[:-4]+'_topics.csv', encoding='utf-8')

    return file_name

def keyword_extraction(tweet):
    keywords=[]
    kw = kw_model.extract_keywords(tweet, keyphrase_ngram_range=(1, 1), stop_words=stopwords)
    kw.extend(kw_model.extract_keywords(tweet, keyphrase_ngram_range=(3, 3), stop_words=stopwords, 
                              use_mmr=True, diversity=0.7))
    for (k,v) in kw:
        keywords.append(k)
    
    return ' '.join(list(set(' '.join(list(set(keywords))).split())))


punctuation = '!"$%&\'()*+,-./:;<=>?[\\]^_`{|}~•@' 
stopwords.extend(['avoir', 'pouvoir', 'devoir'])

def deEmojify(text):
    regrex_pattern = re.compile(pattern = "["
        u"\U0001F600-\U0001F64F"
        u"\U0001F300-\U0001F5FF"
        u"\U0001F680-\U0001F6FF"
        u"\U0001F1E0-\U0001F1FF"
        u"\U00002500-\U00002BEF"
        u"\U00002702-\U000027B0"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642"
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f" 
        u"\u3030"
                           "]+", flags = re.UNICODE)
    return regrex_pattern.sub(r'', text)

def preprocessing_final(tweet):
    # nlp = spacy.load('fr_core_news_md')
    # To lowercase
    punctuation = '!"$%&\'()*+,-./:;<=>?[\\]^_`{|}~•@' 
    """function that also performs tokenization, lemmatization and removal of stopwords"""
    tweet = re.sub('(RT\s@[A-Za-z]+[A-Za-z0-9-_]+)', '', tweet)  # remove re-tweet
    tweet = re.sub('(@[A-Za-z]+[A-Za-z0-9-_]+)', '', tweet)  # remove tweeted at
    tweet = re.sub(r'http\S+', '', tweet)   # remove http links
    tweet = re.sub(r'bit.ly/\S+', '', tweet)  # remove bitly links
    tweet = tweet.strip('[link]')   # remove [links]
    tweet = re.sub(r'pic.twitter\S+','', tweet)
    tweet = re.sub('(#[A-Za-z]+[A-Za-z0-9-_]+)', '', tweet)  # remove hash tags
    tweet = tweet.lower()  # lower case
    tweet = re.sub('[' + punctuation + ']+', ' ', tweet)  # strip punctuation
    tweet = re.sub('\s+', ' ', tweet)  # remove double spacing
    tweet = re.sub('([0-9]+)', '', tweet)  # remove numbers
    tweet=deEmojify(tweet)
    # Creating a doc with spaCy
    doc = nlp(tweet)
    lemmas = []
    for token in doc:
        lemmas.append(token.lemma_)
    return " ".join([str(x) for x in lemmas if x.isalpha() and x not in stopwords])