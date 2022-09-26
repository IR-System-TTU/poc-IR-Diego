from tdim import *
from inverted_index import *

if __name__ == '__main__':
  option = input('Choose a retrieval technique: \n (1) Term Document Incidence Matrix, \n (2) Inverted Index \n')
  if option == '1':
    tdim_execute()
  if option == '2':
    ii_execute()