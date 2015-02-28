import json
import nltk
import string

from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.collocations import *

from collections import defaultdict
from collections import Counter

from elasticsearch import Elasticsearch

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

    for item in ids:
        data = ' '.join(ids_hash[item])
        lowers = data.lower()

        bigram_measures = nltk.collocations.BigramAssocMeasures()

        finder = BigramCollocationFinder.from_words(lowers.split())

        finder.apply_freq_filter(2)
        print finder.nbest(bigram_measures.pmi, 10)
        exit()

        #remove the punctuation using the character deletion step of translate
        tokenizer = RegexpTokenizer(r'\w+')
        tokens = tokenizer.tokenize(lowers)
        stopwordset = set(stopwords.words('english'))
        filtered = [w for w in tokens if not w in stopwordset]
        count = Counter(filtered)
        doc = {
            "business_id" : item,
            "word_freq": count.most_common(25)
        }
        exit()
        template = { "create": { "_index": "my_data", "_type": "doc"} }
        res = es.index(index="my_data", doc_type='doc', body=doc)


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
