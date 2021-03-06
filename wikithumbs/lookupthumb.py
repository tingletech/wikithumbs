#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Wikipedia Article Thubnails
===========================

background
----------

https://gist.github.com/tingletech/8643380

"""
import sys
import argparse
from string import Template
import requests
import json
from shove import Shove
from appdirs import user_cache_dir
from pprint import pprint as pp
import logging
import urllib
from time import sleep


def main(argv=None):
    cache = "".join(['file://',user_cache_dir('wikithumbs', 'cdlib')])
    parser = argparse.ArgumentParser(description='wikithumbs')
    parser.add_argument('page_name', nargs=1, help="wikipedia article title")
    parser.add_argument('--loglevel', default='ERROR')
    parser.add_argument('--cache_url',
                        help='database URL to shove to (file://... for files)', 
                        default=cache)
    parser.add_argument('--sparql_url',
                        help='defaults to http://dbpedia.org/sparql/ but http://dbpedia-live.openlinksw.com/sparql/ sometimes works better', 
                        default="http://dbpedia.org/sparql/")
    parser.add_argument('--polite_factor', default=1, help="wait this number of times request time", type=float)

    if argv is None:
        argv = parser.parse_args()
    # set debugging level
    numeric_level = getattr(logging, argv.loglevel.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % argv.loglevel)
    logging.basicConfig(level=numeric_level, )
    logging.debug(argv)
    logging.info(lookup_page_name(argv.page_name[0], argv.cache_url, argv.sparql_url, argv.polite_factor))


def lookup_page_name(page_name, cache_file='file://test', sparql_url='', polite_factor=1):
    """lookup info from cache"""
    page_name = page_name_normalize(page_name)
    logging.info(cache_file)
    logging.info(page_name)
    cache = Shove(cache_file)
    if page_name in cache:
        logging.debug("cache hit")
        return cache[page_name]
    else:
        logging.debug("cache miss")
        res = perform_sparql_query(page_name, sparql_url, polite_factor)
        cache[page_name] = res
        cache.sync()
        return res


def perform_sparql_query(page_name, sparql_url, polite_factor=1):
    """lookup info from dbpedia"""
    page_name = urllib.quote(page_name)
    query = Template("""select * where {
  ?thumbnail dc:rights ?attribution . { SELECT ?thumbnail WHERE {
      <http://dbpedia.org/resource/$resource> <http://dbpedia.org/ontology/thumbnail> ?thumbnail
    } } } LIMIT 1""")
    query = query.substitute(resource=page_name)
    logging.info(query)
    logging.info(sparql_url)
    params = {
        "query": query,
        "default-graph-uri": 'http://dbpedia.org',
        "format": 'application/sparql-results+json',
        "timeout": 5000,
    }
    logging.debug(params)
    res = requests.get(url=sparql_url, params=params)
    res.raise_for_status()
    # added to support python version < 2.7, otherwise timedelta has total_seconds()
    seconds = (res.elapsed.microseconds + (res.elapsed.seconds + res.elapsed.days*24*3600) * 1e6) / 1e6
    logging.info(res.text)
    results = json.loads(res.text)
    out = {}
    if len(results['results']['bindings']) > 0:
        attribution = results['results']['bindings'][0]['attribution']['value']
        thumbnail = results['results']['bindings'][0]['thumbnail']['value']
        thumbnail = thumbnail.replace('200px-','150px-')
        out = {
            "attribution": attribution,
            "thumbnail": thumbnail,
        }
    sleep(seconds * polite_factor)
    logging.debug('waited for {0} seconds'.format(seconds * polite_factor))
    return out


def page_name_normalize(page_name):
    # http://en.wikipedia.org/wiki/Wikipedia:Page_name
    return page_name.replace(' ', '_')


# main() idiom for importing into REPL for debugging
if __name__ == "__main__":
    sys.exit(main())

"""
Copyright © 2014, Regents of the University of California
All rights reserved.

Redistribution and use in source and binary forms, with or without 
modification, are permitted provided that the following conditions are met:

- Redistributions of source code must retain the above copyright notice, 
  this list of conditions and the following disclaimer.
- Redistributions in binary form must reproduce the above copyright notice, 
  this list of conditions and the following disclaimer in the documentation 
  and/or other materials provided with the distribution.
- Neither the name of the University of California nor the names of its
  contributors may be used to endorse or promote products derived from this 
  software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE 
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE 
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR 
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF 
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS 
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE 
POSSIBILITY OF SUCH DAMAGE.
"""
