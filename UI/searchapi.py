import os
import math

from collections import defaultdict
from elasticsearch import Elasticsearch

from pytagcloud import create_tag_image, make_tags
from pytagcloud.lang.counter import get_tag_counts

import webbrowser
import random

def newsearch(query_word):
	result = []
	es = Elasticsearch()
	query1 = {"query": {"wildcard": {"name": {"value": "*" + query_word + "*" } } } }
	res = es.search(index="urban", body=query1)

	if res['hits']['total'] == 0:
		res = es.search(index="champ", body=query1)

	if res['hits']['total'] == 0:
		return 0

	ret = res['hits']['hits']

	temp = defaultdict(int)
	items = []
	for item in ret:
		ids = item['_source']['business_id']
		query2 = {"query":  {"match": {"business_id": ids } } }
		res = es.search(index="alchem", body=query2)

		for item in res['hits']['hits'][0]['_source']['word_freq']:
			items.append(item)
			temp[item['text'].encode('utf-8')] += 1

	words = []

	for item in items:
		t = {}
		scale = 1
		if 'sentiment' not in item:
			continue
		elif 'type' in item['sentiment']:
			if item['sentiment']['type'] == 'positive':
				scale = 1.75
				t['color'] = (0,255,0)
			elif item['sentiment']['type'] == 'negative':
				scale = 1.25
				t['color'] = (255,0,0)
		elif item['sentiment'] == 'positive':
			scale = 1.75
			t['color'] = (0,255,0)
		elif item['sentiment'] == 'negative':
			scale = 1.25
			t['color'] = (255,0,0)
		elif item['sentiment'] == 'neutral':
			t['color'] = (0,0,255)
		else:
			t['color'] = (128,128,128)
		t['tag'] = item['text'].encode('utf-8')
		t['size'] = int( math.ceil( temp[item['text']] * float(item['relevance']) * 30 * scale) )
		words.append(t)

	create_tag_image(words, 'static/cloud_large.jpg', size=(900, 600), fontname='Philosopher')

def search(query_word):
	result = []
	es = Elasticsearch()
	query1 = {"query": {"wildcard": {"name": {"value": "*" + query_word + "*" } } } }
	res = es.search(index="urban", body=query1)

	if res['hits']['total'] == 0:
		res = es.search(index="champ", body=query1)

	if res['hits']['total'] == 0:
		return 0

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

	create_tag_image(tags, 'static/cloud_large.jpg', size=(900, 600), fontname='Lobster')
