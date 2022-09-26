import pandas as pd
from typing import Dict
from numpy import ndarray
import numpy as np
from constants import *
import re

def tdim_execute():
  # get products from csv file
  df = pd.read_csv('gathered-products-detail.csv', encoding='latin1') #encoding is important because we are on windows: https://pyquestions.com/unicodedecodeerror-utf-8-codec-can-t-decode-byte-0x96-in-position-35-invalid-start-byte 
  df = df.reset_index()  # make sure indexes pair with number of rows

  # cleaning up (this might not be necessary in the future)
  product_names = []
  docs = []
  for index, row in df.iterrows():
    stringDoc = ''
    for key in product_keys:
      if key == 'name':
        product_names.append(row[key])
      stringDoc += ' ' + re.sub("[,\[\]]", " ", str(row[key]))
    docs.append(stringDoc)

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
      vectors.append(np.array(term_doc_inc_matrix[term]))

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
      vectors.append(np.array(term_doc_inc_matrix[term]))

    # perform an OR bitwise operation on all vectors
    result: ndarray = np.array([0] * len(docs))
    for vector in vectors:
      result = result | vector
    print(result)

    # Get the matching documents from our corpus with the result
    docs = [doc for doc in result * names_array if doc] # only retrive the product name
    print(docs)
