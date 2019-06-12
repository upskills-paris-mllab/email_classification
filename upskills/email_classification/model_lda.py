from gensim import corpora, models


def train_lda(data, number_topics=7, passes=100):

    dictionary = corpora.Dictionary(data['body_tokens'])
    # convert tokenized documents into a document-term matrix
    corpus = [dictionary.doc2bow(tokens) for tokens in data['body_tokens']]

    # generate LDA model
    ldamodel = models.ldamodel.LdaModel(corpus, num_topics=number_topics, id2word=dictionary, passes=passes)

    return(ldamodel, corpus)
