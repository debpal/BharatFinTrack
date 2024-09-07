# BharatFinTrack

A Python package designed to simplify the process of downloading and analyzing financial data, including indices, stocks, and mutual funds, from India, that is, Bharat.


### Quickstart

```python
>>> import BharatFinTrack
>>> nse_track = BharatFinTrack.NSETrack()
>>> nse_track.indices_category
['broad', 'sectoral', 'thematic', 'strategy']

# get the dictionary of available indices with base date
>>> nse_track.indices_base_date
{'NIFTY 500': '01-Jan-1995',
 'NIFTY 50': '03-Nov-1995',
 'NIFTY IT': '01-Jan-1996',
 'NIFTY BANK': '01-Jan-2000',
 'NIFTY EV & NEW AGE AUTOMOTIVE': '01-Apr-2005',
 'NIFTY INDIA DEFENCE': '01-Apr-2005',
 'NIFTY ALPHA 50': '01-Apr-2005',
 'NIFTY MIDCAP150 MOMENTUM 50': '01-Apr-2005',
 ...}

# get the list of strategy indices
>>> nse_track.indices_name('strategy')
['NIFTY ALPHA 50',
 'NIFTY MIDCAP150 MOMENTUM 50',
 ...]
```


### Easy installation

```
pip install BharatFinTrack
```

### Installation from the GitHub repository

```
pip install git+https://github.com/debpal/BharatFinTrack.git
```


### License

`BharatFinTrack` is released under the MIT License.