# BharatFinTrack

## Analysis Toolkit

| --- | --- |
| Documemt | [![Documentation Status](https://readthedocs.org/projects/bharatfintrack/badge/?version=latest)](https://bharatfintrack.readthedocs.io/en/latest/?badge=latest) |


## What is BharatFinTrack?
BharatFinTrack is a Python package designed to simplify the process of downloading and analyzing financial data from India, that is Bharat. The current features of the package include:

- **NSE Indices**
  - Access to characteristics of indices.
  - Download of historical daily Total Return Index (TRI) values.


## Easy Installation

To install `BharatFinTrack`, use pip:

```bash
pip install BharatFinTrack
```

## Quickstart
Here’s a brief example of how to use `BharatFinTrack`:

```python
>>> import BharatFinTrack
>>> nse_track = BharatFinTrack.NSETrack()
>>> nse_track.indices_category
['broad', 'sectoral', 'thematic', 'strategy']

# get the list of downloadable indices
>>> nse_track.downloadable_indices
['NIFTY 500',
 'NIFTY 50',
 'NIFTY IT',
 'NIFTY BANK',
 ...]

# get the dictionary of indices base date
>>> nse_track.indices_base_date
{'NIFTY 500': '01-Jan-1995',
 'NIFTY 50': '03-Nov-1995',
 'NIFTY IT': '01-Jan-1996',
 'NIFTY BANK': '01-Jan-2000',
 ...}
```


## Documentation
For detailed information, see the [documentation](https://bharatfintrack.readthedocs.io/en/latest/).


## Development status

The project is in the conceptualization and planning phases.


## License

`BharatFinTrack` is released under the MIT License.