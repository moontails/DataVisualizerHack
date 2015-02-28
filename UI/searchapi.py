import os
from collections import defaultdict
from elasticsearch import Elasticsearch

from pytagcloud import create_tag_image, make_tags
from pytagcloud.lang.counter import get_tag_counts

import webbrowser
import random
def search(query_word):
	result = []
	es = Elasticsearch()
	query1 = {"query": {"wildcard": {"name": {"value": "*" + query_word + "*" } } } }
	res = es.search(index="urban", body=query1)

	if res['hits']['total'] == 0:
		res = es.search(index="champ", body=query1)

	if res['hits']['total'] == 0:
		return

	ret = res['hits']['hits']

	temp = defaultdict(int)
	for item in ret:
		ids = item['_source']['business_id']
		query2 = {"query":  {"match": {"business_id": ids } } }
		res = es.search(index="my_data", body=query2)

		for item in res['hits']['hits'][0]['_source']['word_freq']:
			temp[item[0]] += item[1]

	words = []
	for item in temp:
		words.append((item,temp[item]))

	tags = make_tags(words, maxsize=80)

	#unique name for the jpg - unique name
	rand_num = random.random()
	create_tag_image(tags, 'static/cloud_large.jpg', size=(900, 600), fontname='Lobster')
