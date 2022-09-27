from typing import Dict
from numpy import ndarray
import numpy as np

from helpers import read_csv_and_cleanup

def tdim_execute():
  docs, product_names = read_csv_and_cleanup('gathered-products-detail')

  # Gather the set of all unique terms
  unique_terms = { term for doc in docs for term in doc.split() }

  # Construct a term document incidence matrix
  term_doc_inc_matrix: Dict[str, list[int]] = {}

  for term in unique_terms:
    term_doc_inc_matrix[term] = []

    for doc in docs:
      if term in doc:
        term_doc_inc_matrix[term].append(1)
      else:
        term_doc_inc_matrix[term].append(0)

  names_array = np.array(product_names, dtype='object')

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

    # construct our vector list based on the input terms from the user
    vectors: list[ndarray] = []
    for term in terms:
      if term in term_doc_inc_matrix:
        vectors.append(np.array(term_doc_inc_matrix[term]))

    if len(vectors) == 0:
      return 0

    # perform an AND bitwise operation on all vectors
    result = np.array([1] * len(docs))
    for vector in vectors:
      result = result & vector
    print(result)

    # Get the matching documents from our corpus with the result
    docs = [doc for doc in result * names_array if doc] # only retrive the product name
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

    # construct our vector list based on the input terms from the user
    vectors: list[ndarray] = []
    for term in terms:
      if term in term_doc_inc_matrix:
        vectors.append(np.array(term_doc_inc_matrix[term]))

    if len(vectors) == 0:
      return 0
      
    # perform an OR bitwise operation on all vectors
    result: ndarray = np.array([0] * len(docs))
    for vector in vectors:
      result = result | vector
    print(result)

    # Get the matching documents from our corpus with the result
    docs = [doc for doc in result * names_array if doc] # only retrive the product name
    print(docs)
