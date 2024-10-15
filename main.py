import os

from classes.corpus_reader import CorpusReader
from classes.constants import Constants

def create_out_dir():
    if not os.path.exists('out'):
        os.makedirs('out')

def remove_partial_index_dir_content():
    if os.path.exists(Constants.partial_indexes_path):
        files = os.listdir(Constants.partial_indexes_path)
        for file_name in files:
            os.remove(os.path.join(Constants.partial_indexes_path, file_name))

def remove_final_index_file():
    if os.path.exists(Constants.final_index_path):
        os.remove(Constants.final_index_path)

def main():
    create_out_dir()
    # remove_partial_index_dir_content()
    remove_final_index_file()
    # CorpusReader.create_partial_indexes()
    CorpusReader.create_final_index()


main()
