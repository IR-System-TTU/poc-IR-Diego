import os

import pandas as pd
from string import punctuation
import re
import nltk
from nltk.stem.porter import PorterStemmer
p_stemmer = PorterStemmer()
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))
import itertools
from collections import defaultdict
import streamlit as st

##########################################################################################################

# reads the file
df = pd.read_csv("walmart-products-modified.csv", encoding='latin1')


#########################################################################################################



# the different zones (tables) to create the inverted-indexes
terms_dictionary_for_zone = {
        'name': { },
         'type_of': { },
         'comments': { }
         }


##########################################################################################################



def stemmed_inverted_index_from_data(
    
    # the dataframe
    doc_database # list[str,]
):
    for zone in doc_database.columns:
        # only doing indexing for the chosen zones above
        if zone in terms_dictionary_for_zone.keys():
            # saving docID and the row content for the chosen zones
            for docID, doc in enumerate(df[zone]): # int, str; list[(int, str), ]
                
                # tokenises the words in the row of the selected zone based on NLTK vocab
                sentence_doc = word_tokenize(str(doc)) # list[str,];
                # stems all words in doc
                sentence_str_1 = [p_stemmer.stem(word_tk) for word_tk in sentence_doc]  # list[str,]
                # joins the stemmed tokens back into a sentence for further procesing
                sentence_str_1 = " ".join(sentence_str_1) # str

                # subs all symbols/punctuations (including space) with a space (' '); excludes digits
                sentence_str_1 = re.sub(r'\W+', ' ',sentence_str_1)
                # subs all digits with a space (' '); a sequence of digits (without space) is given one (' ')
                sentence_str_1 = re.sub(r'\d+', ' ',sentence_str_1)
                # subs all symbols AND digits (including spaces) with a space (' '); includes digits
                sentence_str_1 = re.sub(r'[^a-zA-Z]', ' ',sentence_str_1)
                # compiles a pattern and subs out the pattern in sentence_str_1 with ' '
                sentence_str_1 = re.compile('(\s*)pron(\s*)').sub(' ', sentence_str_1)

                # tokenize to clean up one more time if 're' has introduced and garbage
                sentence_doc_1 = word_tokenize(sentence_str_1) # list[str,]
                # strip removes whitespace at beginning and end of string (not in between)
                sentence_str_2 = [str(word_tk_1).strip() for word_tk_1 in sentence_doc_1] # list[str,]
                # strings with >=2 chars only
                sentence_str_2  = [word_str for word_str in sentence_str_2 if len(word_str) >= 2] # list[str,]
                # strings which are not symbols/punctuations
                sentence_str_2 = [word_str for word_str in sentence_str_2  if word_str not in punctuation]
                # strings which are not stop-words; check with: Spacy_Eng.vocab['word'].is_stop
                sentence_str_2 = [word_str for word_str in sentence_str_2 if word_str not in stop_words]

                for term in sentence_str_2: # 'str'
                    # for each zone the term increased in doc freq and appends the posting list if term exists
                    if term in terms_dictionary_for_zone[zone]:
                        terms_dictionary_for_zone[zone][term][0] += 1 # int; doc freq
                        terms_dictionary_for_zone[zone][term][1].append(docID) # list[int,]
                    # if term doesnt exist, put doc freq as 1 and append the first posting list
                    else:
                        terms_dictionary_for_zone[zone][term] =[[],[]] # list[[int], [int, ]]; list[[doc freq], [docIds,]]
                        terms_dictionary_for_zone[zone][term][0] = 1 # int; doc freq
                        terms_dictionary_for_zone[zone][term][1].append(docID)
    # return the inverted-index dictionary
    return terms_dictionary_for_zone




##########################################################################################################


inverted_index_zonal_dictionary = stemmed_inverted_index_from_data(df)



##########################################################################################################
def query_processing(
    query # str
):
    if query == '':
        return None, None
    posting_list = [] # list[]
    # split long string of query terms into into different individual terms based on whitespace
    # query_terms = query.split() #list[str, ]
    each_term = 0 # int
                
    # tokenises the words in the row of the selected zone based on NLTK vocab
    sentence_doc = word_tokenize(str(query)) # list[str,];
    # stems all words in doc
    sentence_str_1 = [p_stemmer.stem(word_tk) for word_tk in sentence_doc]  # list[str,]
    # joins the stemmed tokens back into a sentence for further procesing
    sentence_str_1 = " ".join(sentence_str_1) # str

    # subs all symbols/punctuations (including space) with a space (' '); excludes digits
    sentence_str_1 = re.sub(r'\W+', ' ',sentence_str_1)
    # subs all digits with a space (' '); a sequence of digits (without space) is given one (' ')
    sentence_str_1 = re.sub(r'\d+', ' ',sentence_str_1)
    # subs all symbols AND digits (including spaces) with a space (' '); includes digits
    sentence_str_1 = re.sub(r'[^a-zA-Z]', ' ',sentence_str_1)
    # compiles a pattern and subs out the pattern in sentence_str_1 with ' '
    sentence_str_1 = re.compile('(\s*)pron(\s*)').sub(' ', sentence_str_1)

    # tokenize to clean up one more time if 're' has introduced and garbage
    sentence_doc_1 = word_tokenize(sentence_str_1) # list[str,]
    # strip removes whitespace at beginning and end of string (not in between)
    sentence_str_2 = [str(word_tk_1).strip() for word_tk_1 in sentence_doc_1] # list[str,]
    # strings with >=2 chars only
    sentence_str_2  = [word_str for word_str in sentence_str_2 if len(word_str) >= 2] # list[str,]
    # strings which are not symbols/punctuations
    sentence_str_2 = [word_str for word_str in sentence_str_2  if word_str not in punctuation]
    # strings which are not stop-words; check with: Spacy_Eng.vocab['word'].is_stop
    sentence_str_2 = [word_str for word_str in sentence_str_2 if word_str not in stop_words]

    
    for term in sentence_str_2[:]: # str       
        # for individual terms compute edit distance with each term in the 'name' inverted-index dictionary
        # this is useful if there is a typo in one or multiple of the query terms
        edit_dist_list = [[key, nltk.edit_distance(term, key)]  for key in inverted_index_zonal_dictionary['name']] # list[[str, double], ]
        edit_dist_list_1 = list(zip(*edit_dist_list)) # list[(str,)(double,)]
        # choose the min edit distance as the closest term match in the inverted-index dictionary
        if min(edit_dist_list_1[1]) >=2:
            print('No matching results')
            return 0, 0


        internal_query = edit_dist_list_1[0][edit_dist_list_1[1].index(min(edit_dist_list_1[1]))] # str


        # from the term matched in the inverted-index, append, its posting list to 'posting-list'
        posting_list.append(list(inverted_index_zonal_dictionary['name'][internal_query][1])) # list[[int, ], ]
        each_term +=1

    # for mutltiple query terms, the highest priority posting lists are ones which has ALL the terms in the query (AND query) 
    posting_list_combined_for_and_high_priority = set.intersection(*map(set, posting_list)) # set[int, ]
    posting_list_combined_for_and_high_priority = list(posting_list_combined_for_and_high_priority) # list[int, ]

    # for multiple query terms, we also get (OR query)
    posting_list_combined = list(itertools.chain(*posting_list)) # list[int, ]
    posting_list_combined_for_or_low_priority = set(posting_list_combined) # set[int, ]
    posting_list_combined_for_or_low_priority = list(posting_list_combined_for_or_low_priority)

    # we append the OR query after the AND query as OR is deemed as lower priority here
    for docID_low_priority in posting_list_combined_for_or_low_priority: # int
        if docID_low_priority not in posting_list_combined_for_and_high_priority:
            posting_list_combined_for_and_high_priority.append(docID_low_priority) # list[int,]

    # return the posting list from above
    act_docs = pd.DataFrame(df.loc[posting_list_combined_for_and_high_priority])
    for docID_of_cur_term in posting_list_combined_for_and_high_priority:
        print(pd.DataFrame(df.loc[docID_of_cur_term]))
    return posting_list_combined_for_and_high_priority, act_docs
##########################################################################################################


st.header("Wahmart: Search for items")


query = st.text_input("Type here"," ")
all_postings, act_docs = query_processing(query)


st.write('items:\n',act_docs)
st.write('postings list: \n', all_postings)



