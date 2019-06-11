from bs4 import BeautifulSoup
from collections import defaultdict
import re

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
    for text in texts:
        for token in text:
            frequency[token] += 1

    return [[token for token in text if frequency[token] > count_threshold] for text in texts ]
