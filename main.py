import json
import os
import time

from classes.document import Document
from classes.indexer import Indexer

documents_path = "assets/MEDLINE_2024_Baseline.jsonl"
partial_indexes_path = "partial_indexes"
final_index_path = "final_index.json"
documents_per_index_limit = 10000


def save_partial_index(index):
    if not os.path.exists(partial_indexes_path):
        os.makedirs(partial_indexes_path)

    timestamp = str(time.time()).replace(".", "")
    index_path = partial_indexes_path + "./index-" + timestamp + ".json"

    file = open(index_path, "a")
    file.write(json.dumps(index))


def remove_partial_index_dir_content():
    if os.path.exists(partial_indexes_path):
        files = os.listdir(partial_indexes_path)
        for file_name in files:
            os.remove(os.path.join(partial_indexes_path, file_name))


def create_partial_indexes():
    print("Creating partial indexes...")
    with open(documents_path, "r") as file:
        # i = 0
        documents = []
        line = file.readline()
        while line:
            # print(i)
            line = file.readline()
            document = Document(line)
            documents.append(document)

            if len(documents) >= documents_per_index_limit:
                print("Indexing documents...")
                index = Indexer.index_documents(documents)
                documents = []
                # print(index)
                save_partial_index(index)
            # i += 1
    file.close()


def remove_final_index_file():
    if os.path.exists(final_index_path):
        os.remove(final_index_path)


def create_final_index():
    print("Creating final index...")
    final_index = {}
    ordered_index = {}

    partial_indexes_files = os.listdir(partial_indexes_path)

    # iterate over every file in the partial_indexes directory
    for partial_index_file_name in partial_indexes_files:
        partial_index_file_path = os.path.join(partial_indexes_path, partial_index_file_name)

        # open the file and read the content
        with open(partial_index_file_path, "r") as partial_index_file:
            print("Reading " + partial_index_file_name)
            partial_index = json.loads(partial_index_file.read())
            # merge the final index with the current index
            final_index = Indexer.merge_indexes([final_index, partial_index])

    # sort the keys and the posting lists of the final index
    for key in sorted(final_index.keys()):
        ordered_index[key] = sorted(final_index[key])

    # print("final_index", final_index)

    # write the ordered index to fs
    with open(final_index_path, "a") as file:
        file.write(json.dumps(ordered_index))
    file.close()

    print("Final index saved to file.")


def main():
    remove_partial_index_dir_content()
    remove_final_index_file()
    create_partial_indexes()
    create_final_index()


main()
