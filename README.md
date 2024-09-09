# BharatFinTrack

## What is BharatFinTrack?
BharatFinTrack is a Python package designed to simplify the process of downloading and analyzing financial data from India, that is Bharat. The current features of the package include:

- **NSE Indices**
  - Access to characteristics of indices.


## Easy Installation

To install, use pip:

```bash
pip install BharatFinTrack
```

## Quickstart
A brief example of how to start:

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

## Toolkit

| Feature | Badge|
| --- | --- |
| Version | ![PyPI - Version](https://img.shields.io/pypi/v/BharatFinTrack) |
| Staus | ![PyPI - Status](https://img.shields.io/pypi/status/BharatFinTrack) |
| License | ![PyPI - License](https://img.shields.io/pypi/l/BharatFinTrack) |
| Documemt | [![Documentation Status](https://readthedocs.org/projects/bharatfintrack/badge/?version=latest)](https://bharatfintrack.readthedocs.io/en/latest/?badge=latest) |
