# BharatFinTrack

BharatFinTrack is a Python package whose concept originated on September 1, 2024. 
It is designed to simplify the process of downloading and analyzing financial data from India, that is Bharat. The features of the package include:

* [Nifty Indices](https://www.niftyindices.com/)

    - Provides access to the characteristics of NSE equity indices.
    - Facilitates downloading TRI (Total Return Index) data for all NSE equity indices.
    
    
## Roadmap

* Add support for downloading equity index price data without dividend reinvestment.
* Provide a summary of daily updated values of equity index price data.
* Include NAV (Net Asset Value) data for mutual funds.
* Include NAV data for the National Pension System (NPS).


## Easy Installation

To install, use pip:

```bash
pip install BharatFinTrack
```

## Quickstart
A brief example of how to start:

```python
>>> import BharatFinTrack
>>> nse_product = BharatFinTrack.NSEProduct()
>>> nse_product.equity_index_category
['broad', 'sector', 'thematic', 'strategy', 'variant']

# get the list of all NSE equity indices
>>> nse_product.all_equity_indices
['NIFTY 100',
 'NIFTY 200',
 'NIFTY 50',
 'NIFTY 50 ARBITRAGE',
 ...]

# download TRI data for a specified NSE equity index
>>> nse_tri = BharatFinTrack.NSETRI()
>>> nse_tri.download_historical_daily_data(
        index='NIFTY 50',
        start_date='23-SEP-2024',
        end_date='27-SEP-2024'
    )
	      Date	   Close
------------------------
0	2024-09-23	38505.51
1	2024-09-24	38507.55
2	2024-09-25	38602.21
3	2024-09-26	38916.76
4	2024-09-27	38861.64
```

## Documentation
For detailed information, see the [documentation](http://bharatfintrack.readthedocs.io/).


## Toolkit

| <big>Status</big> | <big>Description</big> |
| --- | --- |
| **PyPI**| ![PyPI - Version](https://img.shields.io/pypi/v/BharatFinTrack) ![PyPI - Status](https://img.shields.io/pypi/status/BharatFinTrack) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/BharatFinTrack) ![PyPI - Wheel](https://img.shields.io/pypi/wheel/BharatFinTrack) |
| **GitHub** | ![GitHub last commit](https://img.shields.io/github/last-commit/debpal/BharatFinTrack) [![flake8](https://github.com/debpal/BharatFinTrack/actions/workflows/linting.yml/badge.svg)](https://github.com/debpal/BharatFinTrack/actions/workflows/linting.yml)	[![mypy](https://github.com/debpal/BharatFinTrack/actions/workflows/typing.yml/badge.svg)](https://github.com/debpal/BharatFinTrack/actions/workflows/typing.yml) [![pytest](https://github.com/debpal/BharatFinTrack/actions/workflows/testing.yml/badge.svg)](https://github.com/debpal/BharatFinTrack/actions/workflows/testing.yml) ![GitHub repo size](https://img.shields.io/github/repo-size/debpal/BharatFinTrack) |
| **Codecov** | [![codecov](https://codecov.io/github/debpal/BharatFinTrack/graph/badge.svg?token=6DIYX8MUTM)](https://codecov.io/github/debpal/BharatFinTrack) |
| **Read** _the_ **Docs** | [![Documentation Status](https://readthedocs.org/projects/bharatfintrack/badge/?version=latest)](https://bharatfintrack.readthedocs.io/en/latest/?badge=latest) |
| **PePy** | ![Pepy Total Downloads](https://img.shields.io/pepy/dt/BharatFinTrack) |
| **License** | ![PyPI - License](https://img.shields.io/pypi/l/BharatFinTrack) |
