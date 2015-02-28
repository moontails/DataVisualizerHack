import json
from elasticsearch import Elasticsearch

def save_chambana():
    es = Elasticsearch()

    query1 = {"query": {"match": {"city": "Urbana" } } }
    query2 = {"query": {"match": {"city": "Champaign" } } }
    res1 = es.search(index="business", body=query1, size=300)
    res2 = es.search(index="business", body=query2, size=400)

    print("Got %d Hits:" % res1['hits']['total'])
    print("Got %d Hits:" % res2['hits']['total'])

    urban = open('urban.json','w')
    champ = open('champ.json','w')

    template = { "create": { "_index": "urban", "_type": "doc"} }
    for hit in res1['hits']['hits']:
        json.dump(template,urban)
        urban.write("\n")

        json.dump(hit['_source'],urban)
        urban.write('\n')

    template = { "create": { "_index": "champ", "_type": "doc"} }
    for hit in res2['hits']['hits']:
        json.dump(template,champ)
        champ.write("\n")

        json.dump(hit['_source'],champ)
        champ.write('\n')

def search():
    es = Elasticsearch()

    query1 = {"query": {"match": {"city": "Urbana" } } }
    query2 = {"query": {"match": {"city": "Champaign" } } }
    res1 = es.search(index="business", body=query1, size=300)
    res2 = es.search(index="business", body=query2, size=400)

    print("Got %d Hits:" % res1['hits']['total'])
    print("Got %d Hits:" % res2['hits']['total'])

    urban = []
    champ = []

    for hit in res1['hits']['hits']:
        urban.append(hit['_source']['business_id'])

    for hit in res2['hits']['hits']:
        champ.append(hit['_source']['business_id'])

    reviews = []

    for ids in urban:
        query = {"query": {"match": {"business_id": ids } } }
        res = es.search(index="reviews", body=query)
        count = res['hits']['total']
        #print("Got %d Hits:" % res['hits']['total'])
        res = es.search(index="reviews", body=query, size=count+1)

        for hit in res['hits']['hits']:
            reviews.append(hit['_source'])
    print len(reviews)
    for ids in champ:
        query = {"query": {"match": {"business_id": ids } } }
        res = es.search(index="reviews", body=query)
        count = res['hits']['total']
        #print("Got %d Hits:" % res['hits']['total'])
        res = es.search(index="reviews", body=query, size=count+1)

        for hit in res['hits']['hits']:
            reviews.append(hit['_source'])
    print len(reviews)

    temp = []
    for item in reviews:
        temp.append(item['business_id'])
    print len(temp),len(set(temp))
    save_reviews(reviews)

def save_reviews(revs):
    outfile = open("myrevs.json","w")
    template = { "create": { "_index": "myrevs", "_type": "doc"} }
    for item in revs:
        json.dump(template,outfile)
        outfile.write("\n")

        json.dump(item,outfile)
        outfile.write('\n')

if __name__ == "__main__":
    #save_chambana()

    search()
