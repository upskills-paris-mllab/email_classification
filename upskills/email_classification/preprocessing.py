from bs4 import BeautifulSoup
from collections import defaultdict
import re
import pandas as pd
from gensim import utils, corpora
from langdetect import detect_langs
from nltk.stem import WordNetLemmatizer
import nltk
import numpy as np
from stop_words import get_stop_words

nltk.download('wordnet')


# A collection of functions dedicated to preprocess and clean emails
#AuthorizationAlreadyExists : Aurelien BAELDE

"""
This first section deals with function modifying email subjects
"""


def remove_prefix(subject: str) -> str:
    """Remove "Re" : and "fwd :" from email subject, being Upper or Lower.

    Args:
        subject: email subject

    Returns:
        subject without prefixes
    """
    return re.sub(r"(\b[Ff][Ww][Dd]?\b|\b[Rr][Ee]\b).?: ", "", subject)


"""
This first section deals with function modifying email body
"""


def remove_html_from_body(body: str) -> str:
    """Remove all html tags and text in a string.

    Args:
        body: email body to clean from html code

    Returns:
        cleaned email body from html
    """
    soup = BeautifulSoup(body, features="html.parser")
    return soup.get_text()


def remove_previous_mail_adress(body: str) -> str:
    """Remove previous email adresses in email body (french and english).

    Args:
        body: email body

    Returns:
        cleaned email body from previous email adresses
    """
    return re.sub(r"(From|De.): .*?(Subject|Objet.):.", "", body)


def remove_regex_patterns(body: str, patterns: list) -> str:
    """Remore string parts given by a list of regex patterns

    Args:
        body: text to clean
        patterns: list of regex pattern to apply

    Returns:
        cleaned text
    """

    for pattern in patterns:
        body = re.sub(pattern, "", body)

    return body


def word_frequency_filter(texts: list, count_threshold: int):
    """Remove word whose frequency is less than a count threshold

    Args:
        texts: collection of texts
        count_threshold: minimal number of word occurence to be kept

    Returns:
        list of documents without word of small occurrence
    """


    frequency = defaultdict(int)
    for text in data["body_tokens"]:
        for token in text:
            frequency[token] += 1

    return [[token for token in text if frequency[token] > count_threshold] for text in texts ]

def clean_message(message: str) :
    # Message pre processing

    minimal_character = 70
    max_count = 70
    count = 0

    # Email specific expressions to remove
    patterns = ["CONFIDENTIAL NOTE.*", "_", "(Get|Sent).*<"]

    clean_body = message
    # Remove all URL links
    body_linkless = re.sub(r"http\S+", "", clean_body)
    body_linkless = re.sub(r"www+", "", body_linkless)
    # Remove html code
    body_linkless = remove_html_from_body(body_linkless)
    # Remove email redundant fields
    body_linkless = remove_previous_mail_adress(body_linkless)
    # Remove email subject abbreviations
    body_linkless = remove_prefix(body_linkless)
    # Remove other specific email parts through regex
    body_linkless = remove_regex_patterns(body_linkless, patterns)

    # Save only if contains minimal token number
    if len(body_linkless) > minimal_character:
        return body_linkless
    else:
        return clean_body

    '''
        # detect language of the message
        if detect_langs(body_linkless)[0].lang == "en":
            cleaned_msg[count] = body_linkless
    '''


def cleaning(data) :
    data['Body'] = data['Body'].apply(clean_message)

    return data


def tokenize_message(message: str, en_stop: list, wordnet_lemmatizer):
    tokens = utils.simple_preprocess(message, min_len=3)
    # remove stop words from tokens
    stopped_tokens = [i for i in tokens if (not i in en_stop)]
    # stem tokens
    stemmed_tokens = [wordnet_lemmatizer.lemmatize(i, pos="v") for i in stopped_tokens]

    return stemmed_tokens


def tokenize(data, count_threshold: int):
    """
    Takes a dataframe containing Subjects and Body and add columns to the df containing lemmetized tokens for each field of each mail
    """

    wordnet_lemmatizer = WordNetLemmatizer()
    en_stop = get_stop_words('en')
    en_stop.append("com")
    en_stop.append("www")

    # We fill the lists with lemmatized tokens
    data['body_tokens'] = [tokenize_message(message, en_stop, wordnet_lemmatizer) for message in data['Body']]

    # We build the frequency map
    frequency = defaultdict(int)
    for text in data["body_tokens"]:
        for token in text:
            frequency[token] += 1

    # We exclude the least used words
    data['body_tokens'] = data['body_tokens'].apply(lambda token_list: [token for token in token_list if frequency[token] > count_threshold])

    return data


def merge_emails(full_data) :
    """
    For each mail we fetch all the mails with the same subject, we take the most recent mail as a basis and we add
    the content of the older mails in its body if it's not already contained in the mail

    Args:
        DataFrame full_data containing the data extracted from the .csv of the emails

    Returns:
        DataFrame unique_data containing the merged mails
    """
    # To remove an anwanted warning
    pd.options.mode.chained_assignment = None

    # Removes caps and "Re","Fwd"
    full_data['Subject'] = [remove_prefix(str(x)) for x in full_data['Subject']]

    to_drop = []
    to_keep = []

    for index, row in full_data.iterrows():

        if (index not in to_drop and index not in to_keep):
            same_subject_df = full_data.loc[full_data['Subject'] == row['Subject']]

            if len(same_subject_df) > 1:
                most_recent_index = same_subject_df.index[-1]
                to_keep.append(most_recent_index)

                most_recent = same_subject_df.loc[most_recent_index]

                for s_index, s_row in same_subject_df.iterrows():
                    if s_index != most_recent_index:
                        if s_row["Body"] not in most_recent["Body"]:
                            most_recent["Body"] += " " + s_row["Body"]

                        to_drop.append(s_index)

            else:
                to_keep.append(index)

    unique_data = full_data.drop(to_drop)

    return unique_data
