import json
import nltk
import string

from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer

from collections import defaultdict
from collections import Counter

from elasticsearch import Elasticsearch

from alchemyapi import AlchemyAPI

def process_json(filename):
    result = []

    infile = open(filename,"r")

    for line in infile:
        temp = json.loads( line.strip() )
        if 'create' in temp:
            continue
        result.append(temp)

    return result

def nlp_process(ids,ids_hash):
    #instantiate an elasticsearch client
    es = Elasticsearch()

    #instantiate an alchemy client
    alchemyapi = AlchemyAPI()

    for item in ids:
        data = ' '.join(ids_hash[item])
        lowers = data.lower()
        alchem_data = []

        response = alchemyapi.keywords('text', lowers, {'sentiment': 1})

        if response['status'] == 'OK':
            print('#Success#')
            for keyword in response['keywords']:
                al_temp = defaultdict()

                al_temp['text'] = keyword['text'].encode('utf-8')
                al_temp['relevance'] = keyword['relevance']
                al_temp['sentiment'] = keyword['sentiment']['type']

                if 'score' in keyword['sentiment']:
                    al_temp['score'] = keyword['sentiment']['score']

                alchem_data.append(al_temp)
        else:
            print('Error in keyword extaction call: ', response['statusInfo'])
        print len(alchem_data)
        # prepare body for insertion
        doc = {
            "business_id" : item,
            "word_freq": alchem_data
        }
        exit()
        template = { "create": { "_index": "alchem", "_type": "doc"} }
        res = es.index(index="alchem", doc_type='doc', body=doc)

if __name__ == "__main__":
    urban = process_json('urban.json')
    champ = process_json('champ.json')
    revs = process_json('myrevs.json')

    print len(urban),len(champ),len(revs)

    ids_hash = defaultdict(list)
    ids = []

    for item in urban:
        ids.append(item['business_id'])

    for item in champ:
        ids.append(item['business_id'])

    print len(ids)

    for item in revs:
        ids_hash[item['business_id']].append(item['text'])

    print len(ids_hash)

    nlp_process(ids,ids_hash)
