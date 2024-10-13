import json


class Document:
    def __init__(self, doc: str):
        try:
            parsed_doc = json.loads(doc)
            self.id = parsed_doc["doc_id"]
            self.text = parsed_doc["text"]
        except Exception as error:
            print(error)
            self.id = None
            self.text = None
