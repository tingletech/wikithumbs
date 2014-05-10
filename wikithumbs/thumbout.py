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
import requests


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
        thumbnail = correct_url(thumb)
        if thumbnail is not None:
            xmlout = open(output_file, 'w')
            xmlout.write(xml_template(xml_escape_url(identity),
                         xml_escape_url(thumbnail),
                         xml_escape_url(thumb['attribution'])).encode('utf8'))
            xmlout.close()


def xml_escape_url(url):
    return url.replace('&','&amp;').replace("'", '&apos;')


def xml_template(identity, thumbnail, attribution):
    return u"""<nail id='{0}'
  thumb='{1}'
  rights='{2}'/>""".format(identity, thumbnail, attribution)


def correct_url(thumb):
    """
    correct_url

    link checker and guesser for wikipedia thunbnail URLs
    :thumb: dict with 'thubmnail' and 'attribution' URLs

    returns a checked (good) URL as a unicode string or None
    """
    url = thumb['thumbnail']
    urlres = requests.head(url)
    # thubmnail URL looks good (check the link first)
    if (urlres.status_code == requests.codes.ok):
        return url

    # something is not right
    # if the attribute page for the image does not exist, then we
    # won't find a thumbnail, so we may as well give up now
    rights = thumb['attribution']
    rightsres = requests.head(rights)
    if (rightsres.status_code != requests.codes.ok):
        return None

    # okay, there should be a good thumbnail here, just not at the
    # URL we tried

    elif (urlres.status_code == 404):
        return correct_url_404(url)
    elif (urlres.status_code == 500):
        return correct_url_500(url)
    # not sure we can get here, something might be very wrong
    else:
        raise Exception("wikipedia thumbnail URL {0} had unexpected status code {1}".format(urlres.status_code,
                                                                                            url))


def correct_url_404(url):
    # try english wikipedia
    url = url.replace('/commons/','/en/',1)
    res = requests.head(url)
    if (res.status_code == requests.codes.ok):
        return url
    elif (res.status_code == 500):
        return correct_url_500(url)
    # not sure we can get here, but don't panic if we do
    else:
        return None


def correct_url_500(url):
    # a 500 usually means the size we requested is too large
    for size in ['100','75','50','25']:
        tryagain = try_smaller_image(url, size)
        if tryagain is not None:
            return tryagain
    # we gave it a shot, but that is one small image!
    return None


def try_smaller_image(url, size):
    string = u''.join(['/', size , 'px-'])
    url = url.replace('/150px-', string, 1)
    res = requests.head(url)
    if (res.status_code == requests.codes.ok):
        return url
    else:
        return None


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
