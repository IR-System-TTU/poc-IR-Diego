from operator import itemgetter
from typing import Dict
import numpy as np

def ii_execute():
  # Collection of documents (corpus)
  review_1 = "The Glider II is a great soccer ball"
  review_2 = "What a bad soccer ball"
  review_3 = "I am happy with the glider"

  docs = [review_1, review_2, review_3]
  
  # Construct an inverted index

  inverted_index: Dict[str, list] = {}

  for i, doc in enumerate(docs):
    for term in doc.split():
      if term in inverted_index:
        inverted_index[term].append(i)
      else:
        inverted_index[term] = [i]

  # # Getting the postings lists for any term
  # posting_list = inverted_index['soccer']
  # print(posting_list)

  # Perform or boolean retrieval
  def or_postings(posting1, posting2):
    p1 = 0
    p2 = 0
    result = list()
    while p1 < len(posting1) and p2 < len(posting2):
      if posting1[p1] == posting2[p2]:
        result.append(posting1[p1])
        p1 += 1
        p2 += 2
      elif posting1[p1] > posting2[p2]:
        result.append(posting2[p2])
        p2 += 1
      else:
        result.append(posting1[p1])
        p1 += 1
    while p1 < len(posting1):
      result.append(posting1[p1])
      p1 += 1
    while p2 < len(posting2):
      result.append(posting2[p2])
      p2 += 1
    res_list = list(itemgetter(*result)(docs))
    print(res_list)

  def and_postings(posting1, posting2):
    p1 = 0
    p2 = 0
    result = list()
    while p1 < len(posting1) and p2 < len(posting2):
      if posting1[p1] == posting2[p2]:
        result.append(posting1[p1])
        p1 += 1
        p2 += 1
      elif posting1[p1] > posting2[p2]:
        p2 += 1
      else:
        p1 += 1

    print(list(itemgetter(*result)(docs))) if len(result) > 1 else print([docs[result[0]]])

  print('Pick: AND or OR Boolean Retrieval')
  retriveal_type = input("Enter 'AND' or 'OR': ")

  if retriveal_type == 'AND':
    print("AND Boolean Retrieval\n")

    pl_1 = inverted_index['great']
    pl_2 = inverted_index['soccer']
    and_postings(pl_1, pl_2)
  else:
    print("OR Boolean Retrieval\n")

    pl_1 = inverted_index['soccer']
    pl_2 = inverted_index['glider']
    or_postings(pl_1, pl_2)



