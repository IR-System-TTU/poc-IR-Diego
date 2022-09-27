from operator import itemgetter
from typing import Dict
from helpers import read_csv_and_cleanup

def ii_execute():
  docs, product_names = read_csv_and_cleanup('gathered-products-detail')
  
  # Construct an inverted index
  inverted_index: Dict[str, Dict[str, int | set]] = {}

  for i, doc in enumerate(docs):
    for term in doc.split():
      if term in inverted_index:
        inverted_index[term]['posting-list'].add(i)
        inverted_index[term]['freq'] = len(inverted_index[term]['posting-list'])
      else:
        inverted_index[term] = {
          'freq': 1,
          'posting-list': {i}
        }

  # Sorting our inverted index alphabetically
  inverted_index = dict(sorted(inverted_index.items(), key=lambda x: x[0].lower()))

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
      
    return result

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

    return result

  print('Pick: AND or OR Boolean Retrieval')
  retriveal_type = input("Enter 'AND' or 'OR': ")

  if retriveal_type == 'AND':
    print("AND Boolean Retrieval\n")

    posting_lists = []
    while True:
      term = input("Enter term: ")
      if term != '.':
        posting_lists.append(list(inverted_index[term]['posting-list']))
      else:
        break

 
    if len(posting_lists) == 0:
      return 0

    # Sort postings lists asc by length (AND query performance improvement)
    sorted_posting_lists = sorted(posting_lists, key=lambda x: len(x))

    result = list()

    for i in range(0, len(sorted_posting_lists), 2):
      pl_1 = sorted_posting_lists[i]
      pl_2 = sorted_posting_lists[i]
      if i + 1 < len(sorted_posting_lists):
        pl_2 = sorted_posting_lists[i + 1]

      result = and_postings(pl_1, pl_2)

    if len(result) == 0:
      return 0
      
    print(list(itemgetter(*result)(product_names))) if len(result) > 1 else print([product_names[result[0]]])

  else:
    print("OR Boolean Retrieval\n")

    posting_lists = []
    while True:
      term = input("Enter term: ")
      if term != '.':
        posting_lists.append(list(inverted_index[term]['posting-list']))
      else:
        break

 
    if len(posting_lists) == 0:
      return 0

    result = list()

    for i in range(0, len(posting_lists), 2):
      pl_1 = posting_lists[i]
      pl_2 = list()
      if i + 1 < len(posting_lists):
        pl_2 = posting_lists[i + 1]

      result = or_postings(pl_1, pl_2)

    if len(result) == 0:
      return 0
      
    print(list(itemgetter(*result)(product_names))) if len(result) > 1 else print([product_names[result[0]]])



