#!/usr/bin/env python3
# Copyright 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
"""Interactive mode for the tfidf DrQA retriever module."""

import argparse
import code
import prettytable
import logging
from drqa import retriever
from elasticsearch import Elasticsearch

es = Elasticsearch()

logger = logging.getLogger()
logger.setLevel(logging.INFO)
fmt = logging.Formatter('%(asctime)s: [ %(message)s ]', '%m/%d/%Y %I:%M:%S %p')
console = logging.StreamHandler()
console.setFormatter(fmt)
logger.addHandler(console)

parser = argparse.ArgumentParser()
parser.add_argument('--model', type=str, default=None)
args = parser.parse_args()

logger.info('Initializing ranker...')
ranker = retriever.get_class('tfidf')(tfidf_path='../DB/simple.npz')


def fetch_elastic_text(doc_id):
    logger.info(doc_id)
    #res = es.get(index="python", doc_type="python", id=doc_id, filter_path=['text'])
    res = es.search(index="htts", doc_type="htts", body={"query":{"bool":{"must":[{"query_string":{"default_field":"documentId.keyword","query":doc_id}}]}}})
    for doc in res['hits']['hits']:
        res = doc['_source']['text']
    return res

# ------------------------------------------------------------------------------
# Drop in to interactive
# ------------------------------------------------------------------------------

def myprocess(query,k=1):
    doc_names,doc_scores = ranker.closest_docs(query,k)
    result = []
    for i in range(len(doc_names)):
        result.append({doc_names[i].split('-')[0] : fetch_elastic_text(doc_names[i])})

    return result


def process(query, k=1):
    doc_names, doc_scores = ranker.closest_docs(query, k)
    table = prettytable.PrettyTable(
        ['Rank', 'Doc Id', 'Doc Score']
    )
    for i in range(len(doc_names)):
        table.add_row([i + 1, doc_names[i], '%.5g' % doc_scores[i]])
    print(table)
    logger.info(fetch_elastic_text(doc_names[0]))
    logger.info(fetch_elastic_text(doc_names[1]))


banner = """
Interactive TF-IDF DrQA Retriever
>> process(question, k=1)
>> usage()
"""


def usage():
    print(banner)


#code.interact(banner=banner, local=locals())
