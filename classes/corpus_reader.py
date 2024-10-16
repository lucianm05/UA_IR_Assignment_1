import json
import os
import time

from classes.document import Document
from classes.indexer import Indexer
from classes.constants import Constants

class CorpusReader:
  @staticmethod
  def save_partial_index(index):
      if not os.path.exists(Constants.partial_indexes_path):
          os.makedirs(Constants.partial_indexes_path)

      timestamp = str(time.time()).replace(".", "")
      index_path = os.path.join(Constants.partial_indexes_path, 'index' + timestamp + '.json')

      file = open(index_path, "a")
      file.write(json.dumps(index))

  @staticmethod
  def create_partial_indexes():
      print("Creating partial indexes...")
    #   partial_index = {}
      documents = []
      with open(Constants.documents_path, "r") as file:
        #   i = 0
          # j = 0
          line = file.readline()
          while line:
              print(len(documents))
              document = Document(line)
              documents.append(document)
            #   document_index = Indexer.index_document(document)
            #   partial_index = Indexer.merge_indexes([partial_index, document_index])

              if len(documents) >= Constants.documents_per_index_limit:
                  print("Saving index...")
                  partial_index = Indexer.index_documents(documents)
                  CorpusReader.save_partial_index(partial_index)
                  documents = []
                #   partial_index = {}
                #   i = 0

            #   i += 1
            #   j += 1
              line = file.readline()
      file.close()

  @staticmethod
  def create_final_index():
      print("Creating final index...")
      final_index = {}
      ordered_index = {}

      partial_indexes_files = os.listdir(Constants.partial_indexes_path)

      # iterate over every file in the partial_indexes directory
      for partial_index_file_name in partial_indexes_files:
          partial_index_file_path = os.path.join(Constants.partial_indexes_path, partial_index_file_name)

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
      with open(Constants.final_index_path, "a") as file:
          file.write(json.dumps(ordered_index))
      file.close()

      print("Final index saved to file.")