import json
from collections import defaultdict
from elasticsearch import Elasticsearch

def read_json(filename):
    with open(filename , 'r') as infile:
        for line in infile:
            print type(line)
            exit()
        data = json.load(infile)
        print type(data)

def load_data(filenames):
    #instantiate an elasticsearch client
    es = Elasticsearch()

    for filename in filenames:
        print "Processing:", filename
        index_name = filename.split('.')[0].split('/')[-1]
        template = { "create": { "_index": index_name, "_type": "doc"} }

        with open(filename, 'r') as infile:
            for line in infile:
                doc = json.loads(line.strip())
                res = es.index(index=index_name, doc_type='doc', body=doc)
    print "Finished processing all files"


def get_business_ids(filename):
    ids = defaultdict()

    with open(filename, 'r') as infile, open('test.json','w') as outfile:
        for lines in infile:
            line = json.loads(lines)
            ids[line['business_id']] = line

    return ids

def get_reviews(filename, ids):
    reviews = defaultdict(list)

if __name__ == "__main__":
    #ids = get_business_ids('yelp_dataset/dataset_business.json')
    #reviews = read_json('yelp_dataset/dataset_review.json')
    input_files = ['yelp_dataset/business.json','yelp_dataset/review.json']

    ids = get_business_ids('yelp_dataset/dataset_business.json')

    reviews = get_reviews('yelp_dataset/review.json', ids)
    # to create json for bulk load into elasticsearch
    #load_data(input_files)
