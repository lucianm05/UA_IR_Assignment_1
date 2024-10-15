import itertools

from classes.tokenizer import Tokenizer
from classes.document import Document

class Indexer:
    @staticmethod
    def __find_posting_by_doc_id(posting_list, doc_id):
        for i, posting in enumerate(posting_list):
            id = Indexer.__get_posting_id(posting)
            if id == doc_id:
                return i
            return None
        
    @staticmethod
    def __get_posting_id(posting):
        parts = posting.split(';')
        return parts[0]

    @staticmethod
    def __get_posting_positions(posting):
        parts = posting.split(';')
        return parts[1]
    
    @staticmethod
    def index_document(document: Document):
        tokens = Tokenizer.tokenize_terms(document.text)
        document_index = {}

        for i, token in enumerate(tokens):
            # create the posting list if it does not exist
            if token not in document_index:
                document_index[token] = []
                # add the document id to the posting list

            # save a reference to the posting_list related to the current token
            posting_list = document_index[token]
            # try to find if there is already an entry with the same document id in the posting_list
            existing_posting_position = Indexer.__find_posting_by_doc_id(posting_list, document.id)

            # if there is already an entry, we need to append the position (i) to the posting
            if existing_posting_position is not None:
                existing_posting = posting_list[existing_posting_position]
                posting_list[existing_posting_position] = existing_posting + "," + str(i) 
            # if there isn't, we need to append the new posting, initializing the document id and the first position (i)
            else:
                posting_list.append(document.id + ";" + str(i))

        return document_index

    @staticmethod
    def index_documents(documents: list[Document]):
        return Indexer.merge_indexes([Indexer.index_document(document) for document in documents])

    @staticmethod
    def merge_posting_lists(posting_lists: list[list[str]]):
        flattened_postings_list = list(itertools.chain.from_iterable(posting_lists))
        postings_dict = {}

        for posting in flattened_postings_list:
            # print('posting', posting)
            doc_id, positions = posting.split(";")
            if doc_id not in postings_dict:
                postings_dict[doc_id] = positions
            else:
                postings_dict[doc_id] = postings_dict[doc_id] + "," + positions
        
        # Convert the dictionary back to the original format
        merged_list = [f"{pmid};{values}" for pmid, values in postings_dict.items()]
        
        return merged_list

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

