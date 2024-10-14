from classes.tokenizer import Tokenizer
from classes.document import Document

tokenizer = Tokenizer()


class Indexer:
    @staticmethod
    def index_document(document: Document):
        tokens = tokenizer.tokenize_terms(document.text)
        document_index = {}

        for token in tokens:
            # create the posting list if it does not exist
            if token not in document_index:
                document_index[token] = []
                # add the document id to the posting list

            document_index[token].append(document.id)

        return document_index

    @staticmethod
    def index_documents(documents: list[Document]):
        return Indexer.merge_indexes([Indexer.index_document(document) for document in documents])

    @staticmethod
    def merge_posting_lists(posting_lists: list[list[str]]):
        merged = set()

        for posting_list in posting_lists:
            merged.update(posting_list)

        return list(merged)

    @staticmethod
    def merge_indexes(indexes: list[dict[str, list[str]]]):
        merged_index = {}

        for index in indexes:
            for token, posting_list in index.items():
                if token not in merged_index:
                    merged_index[token] = posting_list

                elif token in index:
                    merged_index[token] = Indexer.merge_posting_lists([merged_index[token], posting_list])

        return merged_index

