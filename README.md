# Wikipedia Article Thubnails

## background

https://gist.github.com/tingletech/8643380

## Install

```
pip install https://github.com/tingletech/wikithumbs/archive/master.zip
```
or
```
git clone https://github.com/tingletech/wikithumb.git
cd wikithumb
python setup.py install
```

Since we have millions of records we want to look up (every time
we re-index) it should have a local cache of results.

current version just shoves data into cache

```
wikithumbs

positional arguments:
  page_name             wikipedia article title

optional arguments:
  -h, --help            show this help message and exit
  --loglevel LOGLEVEL
  --cache_url CACHE_URL
                        database URL to shove to (file://... for files)
  --sparql_url SPARQL_URL
                        defaults to http://dbpedia.org/sparql/ but http
                        ://dbpedia-live.openlinksw.com/sparql/ sometimes works
                        better

```
