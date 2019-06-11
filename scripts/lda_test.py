from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
import gensim
from sklearn.datasets import fetch_20newsgroups

tokenizer = RegexpTokenizer(r'\w+')

# create English stop words list
en_stop = get_stop_words('en')
en_stop.append("com")
en_stop.append("can")

# Create p_stemmer of class PorterStemmer
p_stemmer = PorterStemmer()

# create sample documents
doc_a = "Brocolli is good to eat. My brother likes to eat good brocolli, but not my mother."
doc_b = "My mother spends a lot of time driving my brother around to baseball practice."
doc_c = "Some health experts suggest that driving may cause increased tension and blood pressure."
doc_d = "I often feel pressure to perform well at school, but my mother never seems to drive my brother to do better."
doc_e = "Health professionals say that brocolli is good for your health."

newsgroups = fetch_20newsgroups(subset="train", shuffle = True)


# compile sample documents into a list
doc_set = newsgroups.data

# list for tokenized documents in loop
texts = []
tagged = []

# loop through document list
for count, doc in enumerate(doc_set):
    print(count/len(doc_set))
    # clean and tokenize document string
    raw = doc.lower()
    #tokens = tokenizer.tokenize(raw)
    tokens = gensim.utils.simple_preprocess(raw)

    # remove stop words from tokens
    stopped_tokens = [i for i in tokens if (not i in en_stop) and (len(i) >= 3)]

    # stem tokens
    stemmed_tokens = [p_stemmer.stem(i) for i in stopped_tokens]

    print(stemmed_tokens)
    # add tokens to list
    texts.append(stemmed_tokens)

# turn our tokenized documents into a id <-> term dictionary
dictionary = corpora.Dictionary(texts)

# convert tokenized documents into a document-term matrix
corpus = [dictionary.doc2bow(text) for text in texts]

# generate LDA model
ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=8, id2word=dictionary, passes=5)

ldamodel.print_topics(num_topics = 8, num_words=10)