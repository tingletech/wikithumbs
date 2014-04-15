#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Wikipedia Article Thubnails
===========================

background
----------

https://gist.github.com/tingletech/8643380

"""
import sys, os
import argparse
import codecs
from shove import Shove
from appdirs import user_cache_dir
from pprint import pprint as pp
import logging
import locale


def main(argv=None):
    cache = "".join(['file://',user_cache_dir('wikithumbs', 'cdlib')])
    parser = argparse.ArgumentParser(description='wikithumbs')
    parser.add_argument('output_dir')
    parser.add_argument('--loglevel', default='ERROR')
    parser.add_argument('--cache_url',
                        help='database URL to shove to (file://... for files)', 
                        default=cache)

    if argv is None:
        argv = parser.parse_args()
    # set debugging level
    numeric_level = getattr(logging, argv.loglevel.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % argv.loglevel)
    logging.basicConfig(level=numeric_level, )
    logging.debug(argv)
    cache = Shove(argv.cache_url)
    export(cache, argv.output_dir.decode(sys.stdin.encoding))


def export(cache, output_dir):
    # crete output dir if it does not exist?
    for identity, thumb in cache.iteritems():
        identity = identity.decode('utf-8')
        logging.debug(identity)
        if not thumb:
            continue
        output_file = os.path.join(output_dir, u''.join([identity, u'.xml']))
        logging.info(output_file)
        xmlout = open(output_file, 'w')
        xmlout.write(xml_template(xml_escape_url(identity), xml_escape_url(thumb['thumbnail']), xml_escape_url(thumb['attribution'])).encode('utf8'))
        xmlout.close()


def xml_escape_url(url):
    return url.replace('&','&amp;').replace("'", '&apos;')


def xml_template(identity, thumbnail, attribution):
    return u"""<nail id='{0}'
  thumb='{1}'
  rights='{2}'/>""".format(identity, thumbnail, attribution)


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
