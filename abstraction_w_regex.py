import pandas as pd
import re
import csv
import sys
from collections import defaultdict
#reload(sys)
import os
#COUNT THE USERS WHO HAVE INSTANCES OF TERMS PRESENT IN TwADR
#TEST IF A STRING IN A REDDIT tweet IS A SUBSTRING OF THE SNOMED-CT CONCEPT AND CHANGE THE REDDIT'S STRING ACCORDINGLY

#abstraction (medical entity normalization code)

def abstract(fpath, ask_lexpath):
    #df = pd.read_csv(fpath, sep='\t', index_col=0)
    df = pd.read_csv(fpath, encoding="iso-8859-1")
    dict_snomed = defaultdict(list)
    with open(ask_lexpath, 'r', encoding="iso-8859-1") as f:
        #reader = csv.reader(f, delimiter = '\t')
        reader = csv.reader(f, delimiter = '\t')
        #reader.next()
        next(reader)
        for key, value in reader:
            #for v in value.replace("['",'').replace("']",'').replace("'",'').split(', '):
            for v in value.replace('["','').replace('"]','').replace('"','').split(', '):
                #v = "string. With. Punctuation?"
                #print(v.lower())
                v = v.lower()
                #v = v.replace(',','')
                
                #v = re.sub(r'[^\w\s]','',v)   #punctuation removal
                print(v)
                dict_snomed[key.lower()].append(v)
        #next(reader)
    #columns_I = ['user','tweet', 'suicide risk', 'tweet_hits']
    columns_I = ['tweet', 'label', 'tweet_hits']

    df_snomed = pd.DataFrame(columns=columns_I)  #dataframe for abstracted tweets
    tweet_new = ''    #commented on 0408
    #tweet_new = list()  #added on 0408
    for i,row in df.iterrows():
        tweet_hits = 0  #number of hits against the lexicon
        tweet = str(row[0]).lower()  #a reddit tweet lowercased
        #print(tweet)
        #tweet = str(row[1]).lower()  #a reddit tweet lowercased
        for snomed, slang in dict_snomed.items():
            for v in slang:
                #if v in tweet:   #if the slang is present anywhere in the tweet
                p = re.compile(v)  #converting a string into a regex pattern
                matches = p.findall(tweet)
                print(v)
                for match in matches:
                    #print(snomed,match)
                    #tweet_new = str(re.sub(r'\b' + str(v) + r'\b', snomed, tweet))   #replace all mentions of the slang in the tweet with the snomed term
                    tweet = tweet.replace(match, snomed)   #added on 0506
                    #print(snomed)
                    tweet_hits += 1
        #df_snomed = df_snomed.append({'user' : row[0] , 'tweet' : tweet, 'suicide risk':row[2] , 'tweet_hits' : tweet_hits}, ignore_index=True)
        df_snomed = df_snomed.append({'tweet' : tweet, 'label':row[1] , 'tweet_hits' : tweet_hits}, ignore_index=True)
    return df_snomed

  #example call to abstraction method
#df_abstract = abstract('Consolidated.csv','cannabis_lexicon.tsv')
df_abstract = abstract('Consolidated.csv','depression_lexicon.tsv')
print(df_abstract)
#df_abstract.to_csv('abstracted_cannabis_consolidated.csv', index=False)
df_abstract.to_csv('abstracted_depression_consolidated.csv', index=False)

'''
df_abstract = abstract('drive/My Drive/off_shoot_WWW19/abstraction/Dr_welton_full_annotations.tsv', 
                       'drive/My Drive/off_shoot_WWW19/abstraction/SNOMED_AskAPatient_Dict.tsv', 'drive/My Drive/off_shoot_WWW19/abstraction/SNOMED_TwADR-L_Dict.tsv')
'''
