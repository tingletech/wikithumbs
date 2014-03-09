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
from pprint import pprint as pp
import requests
import json
import shove
import percache
from shove import Shove
from appdirs import *

_base_ = 'http://dbpedia.org/sparql/'
#_base_ = 'http://dbpedia-live.openlinksw.com/sparql/'


def main(argv=None):
    cache = "".join(['file://',user_cache_dir('wikithumbs', 'cdlib')])
    parser = argparse.ArgumentParser(description='wikithumbs')
    parser.add_argument('page_name', nargs=1, 
        help="wikipedia article title")
    parser.add_argument('--localdata', 
        help="where to keep the local stash")
    parser.add_argument('--loglevel', default='ERROR')
    parser.add_argument('--cache_url',
                        help='database URL to shove to', 
                        default="cache")
    if argv is None:
        argv = parser.parse_args()
    pp(lookup_page_name(argv.page_name[0], cache))


def lookup_page_name(page_name, cache_file='file://test'):
    page_name = page_name_normalize(page_name)
    cache = Shove(cache_file)
    if page_name in cache:
        return cache[page_name]
    else:
        res = perform_sparql_query(page_name)
        cache[page_name] = res
        cache.sync()
        return res        

def perform_sparql_query(page_name):
    query = Template("""select * where {
  ?thumbnail dc:rights ?attribution . { SELECT ?thumbnail WHERE {
      <http://dbpedia.org/resource/$resource> <http://dbpedia.org/ontology/thumbnail> ?thumbnail
    } } } LIMIT 1""")
    query = query.substitute(resource=page_name)
    params = {
        "query": query,
        "default-graph-uri": 'http://dbpedia.org',
        "format": 'application/sparql-results+json',
        "timeout": 5000,
    }
    res = requests.get(url=_base_, params=params)
    print "expensive"
    return json.loads(res.text)

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
