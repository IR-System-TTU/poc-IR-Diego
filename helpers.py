import string
import re
import pandas as pd
from constants import *

def read_csv_and_cleanup(csv_file_name: string) -> tuple[list, list]:
  # get products from csv file
  df = pd.read_csv(f'{csv_file_name}.csv', encoding='latin1') #encoding is important because we are on windows: https://pyquestions.com/unicodedecodeerror-utf-8-codec-can-t-decode-byte-0x96-in-position-35-invalid-start-byte 
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
  
  return docs, product_names