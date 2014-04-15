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

Python 2.6 users will need to `pip install argparse` till [#1](/../../issues/1) is fixed.

Since we have millions of records we want to look up (every time
we re-index) it uses [a python module `shove`](https://bitbucket.org/lcrees/shove/overview)
to store results. And XML, gotta have XML.  One XML file per thubmnail/attribution.

Well, only 88k of the initial 1.9m have wikipedia links.  And ~.5 of those have 
thumbnail hits.

The command line program `lookupthumb` takes a page name as a parameter
and checks if there is an entry in the shove dataebase under that key, and if not
performs a SPARQL query for the thumbnail and attribution link and
records it.

The command line program `thumbout` takes a directory name as a parameter
and outputs an XML file for each lookup that had results into the named
directory.

## lookupthumb

Look up thumbnail and rights for one wikipedia page.  Adds results
to the shove cache.

```
usage: lookupthumb [-h] [--loglevel LOGLEVEL] [--cache_url CACHE_URL]
                   [--sparql_url SPARQL_URL]
                   [--polite_factor POLITE_FACTOR]
                   page_name

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
  --polite_factor POLITE_FACTOR
                        wait this number of times request time
```

xargs does not like single quotes in the input unless you use null terminated strings

```
time xargs -0 -I {} lookupthumb {} < 1%name0.txt
```

## thumbout

create a directory of XML files

```
usage: thumbout [-h] [--loglevel LOGLEVEL] [--cache_url CACHE_URL]
                output_dir

wikithumbs

positional arguments:
  output_dir

optional arguments:
  -h, --help            show this help message and exit
  --loglevel LOGLEVEL
  --cache_url CACHE_URL
                        database URL to shove to (file://... for files)
```

Files are created in `output_dir` and 
and named `page_name`.xml.  They have a format like this

```xml
<nail id='Marc_Seguin'
  thumb='http://upload.wikimedia.org/wikipedia/commons/thumb/0/07/Seguin.jpg/150px-Seguin.jpg'
  rights='http://en.wikipedia.org/wiki/File:Seguin.jpg'/>
```

These will be read into XTF using `document()` in xslt.

