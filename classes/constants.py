class Constants:
  documents_path = "assets/MEDLINE_2024_Baseline.jsonl"
  partial_indexes_path = "out/partial_indexes"
  final_index_path = "out/final_index.json"
  documents_per_index_limit = 10000
  non_tokenizable_terms = ["", "the", "and", "is", "or", "of", "in", "that", "by", "for", "to", "a", "as", "were"]