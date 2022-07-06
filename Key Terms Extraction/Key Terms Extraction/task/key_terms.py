from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk
from lxml import etree
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import Counter
import string

root = etree.parse('news.xml').getroot()
corpus = root[0]

all_news_texts_cleared = {}

for news in corpus:
    news_name = news[0].text
    news_text = news[1].text
    # Tokenization
    news_text_tokenized = word_tokenize(news_text.lower())
    # Lemmatization
    wnl = WordNetLemmatizer()
    news_text_lemmatized = [wnl.lemmatize(word) for word in news_text_tokenized]
    # punctuation and stopwords
    news_text_clear = [word for word in news_text_lemmatized
                       if word not in list(string.punctuation) and word not in stopwords.words('english')]

    # nouns
    news_text_nouns = [word for word in news_text_clear if nltk.pos_tag([word])[0][1] == 'NN']
    all_news_texts_cleared[news_name] = news_text_nouns


# tf-idf
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform([' '.join(text) for text in all_news_texts_cleared.values()]).toarray()
terms = vectorizer.get_feature_names_out()

doc_words_scores = {}
for i, key in enumerate(list(all_news_texts_cleared.keys())):
    doc_words_scores.setdefault(key, {})
    for j, value in enumerate(tfidf_matrix[i]):
        if value > 0:
            word = terms[j]
            doc_words_scores[key][word] = tfidf_matrix[i][j]

# print 5 best words for every document
for key, value in doc_words_scores.items():
    print(f'{key}:')
    value_sorted = sorted(value.items(), key=lambda x: (x[1], x[0]), reverse=True)
    for word, count in value_sorted[:5]:
        print(f'{word}', end=' ')
    print()
