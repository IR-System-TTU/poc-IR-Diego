from typing import Dict
from numpy import ndarray
import numpy as np

# Collection of documents (corpus)
review_1 = "The Glider II is a great soccer ball"
review_2 = "What a bad soccer ball"
review_3 = "I am happy with the glider"

docs = [review_1, review_2, review_3]
 
# Gather the set of all unique terms
unique_terms = np.array([term for doc in docs for term in doc.split()])

# Construct a term-document matrix
term_doc_inc_matrix: Dict[str, list[int]] = {}

for term in unique_terms:
  term_doc_inc_matrix[term] = []

  for doc in docs:
    if term in doc:
      term_doc_inc_matrix[term].append(1)
    else:
      term_doc_inc_matrix[term].append(0)

docs_array = np.array(docs, dtype='object')

print('Pick: AND or OR Boolean Retrieval')
retriveal_type = input("Enter 'AND' or 'OR': ")

if retriveal_type == 'AND':
  print("AND Boolean Retrieval\n")

  terms = []
  while True:
    term = input("Enter term: ")
    if term != '.':
      terms.append(term)
    else:
      break

  vectors: list[ndarray] = []
  for term in terms:
    vectors.append(np.array(term_doc_inc_matrix[term]))

  result = np.array([1] * len(docs))
  for vector in vectors:
    result = result & vector
  print(result)

  # Get the matching documents from our corpus with the result
  docs = [doc for doc in result * docs_array if doc]
  print(docs)
else:
  print("OR Boolean Retrieval\n")

  terms = []
  while True:
    term = input("Enter term: ")
    if term != '.':
      terms.append(term)
    else:
      break

  vectors: list[ndarray] = []
  for term in terms:
    vectors.append(np.array(term_doc_inc_matrix[term]))

  result: ndarray = np.array([0] * len(docs))
  for vector in vectors:
    result = result | vector
  print(result)

  # Get the matching documents from our corpus with the result
  docs = [doc for doc in result * docs_array if doc]
  print(docs)
