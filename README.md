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


## pre-programming design notes

To be called from XSLT (<a href="http://xtf.cdlib.org/">XTF</a>)
so it will need a command line interface.

```bash
prompt$ wikithumb "Charlie Haden"
<figure class="wikipedia_thumbnail">
  <a href="http://en.wikipedia.org/wiki/File:Gilbert_Stuart_Williamstown_Portrait_of_George_Washington.jpg">
    <img src="http://upload.wikimedia.org/wikipedia/commons/thumb/d/d3/Charlie_Haden_-_Pescara_Italy_1990.jpg/200px-Charlie_Haden_-_Pescara_Italy_1990.jpg" alt= "" />
    <figurecaption>Image from Wikipedia</figurecaption>
  </a>
</figure>
```

[should the image be converted to a data-uri or a local cache?]

Since we have millions of records we want to look up (every time
we re-index) it should have a local cache of results.
