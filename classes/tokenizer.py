import re
from classes.constants import Constants
from nltk.stem import PorterStemmer

stemmer = PorterStemmer()

class Tokenizer:
    @staticmethod
    def tokenize_term(term: str):
        # 1. store all tokenized terms as lowercase
        # 2. remove all dots, so both u.s.a. and usa will be queried the same
        token = term \
            .lower()\
            .replace(".", "")\
            .replace(":", "")

        # 3. remove all numbers, we don't want to store them
        token = re.sub(r"\d", "", token)

        if token in Constants.non_tokenizable_terms\
            or token.isalpha() is False\
            or len(token) <= 3:
            return None

        return stemmer.stem(token)

    @staticmethod
    def tokenize_terms(terms: str):
        # 1. remove all commas
        tokens = terms.replace(",", "")
        # 2. split on whitespaces
        tokens = re.split(r"\s+", tokens)
        tokens = [Tokenizer.tokenize_term(term) for term in tokens]

        return [token for token in tokens if token is not None]