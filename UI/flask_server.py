import os
from collections import defaultdict
from flask import Flask
from flask import request
from flask import jsonify
from flask import render_template
from flask import send_file
import ast
import searchapi
from elasticsearch import Elasticsearch
import time

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('dashboard.html')

@app.route('/word_cloud', methods=['POST'])
def word_cloud():
    print "Processing the submitted configurations for Network"
    print request.form['name']
    if searchapi.newsearch(request.form['name']) == 0:
        return render_template('dashboard-error.html')

    return render_template('dashboard-results.html', timestamp = time.time())

if __name__ == '__main__':
	app.debug = True
	app.run()
