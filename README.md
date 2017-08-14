# siteMapGen

*site map generator* - crawls over page and gathers links to internal pages.


## installing

```
pip install -r requirements.txt
```


## running code

Please see help of the main `run.py` script to see how to use this script.

```
python run.py -h
```


## running tests

```
PYTHONPATH=`pwd` python tests/crawler_tests.py
PYTHONPATH=`pwd` python tests/writer_tests.py
PYTHONPATH=`pwd` python tests/run_tests.py
```
