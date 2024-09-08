# BharatFinTrack

A Python package designed to simplify the process of downloading and analyzing financial data from India, that is Bharat.

[![Documentation Status](https://readthedocs.org/projects/bharatfintrack/badge/?version=latest)](https://bharatfintrack.readthedocs.io/en/latest/?badge=latest)


### Easy Installation

To install `BharatFinTrack`, use pip:

```bash
pip install BharatFinTrack
```


### Quickstart
Here’s a brief example of how to use `BharatFinTrack`:

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
 ...}

# get the list of strategy indices
>>> nse_track.indices_name('strategy')
['NIFTY ALPHA 50',
 'NIFTY MIDCAP150 MOMENTUM 50',
 ...]
```

### Present features

- **NSE Indices**
  - Characteristics of indices whose data can be accessed.
  - Download of historical daily Total Return Index (TRI) values.

### Documentation
For detailed information, see the [documentation](https://bharatfintrack.readthedocs.io/en/latest/).


### Development status

The project is in the conceptualization and planning phases.



### License

`BharatFinTrack` is released under the MIT License.