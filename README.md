# BharatFinTrack


`BharatFinTrack` is a Python package designed to simplify the process of downloading and analyzing financial data from India. Conceptualized on September 1, 2024, and launched on September 8, 2024, this package is tailored for long-term investors seeking to streamline their financial data workflows. 

`BharatFinTrack` focuses on open-source financial data, with an initial emphasis on analyzing NSE equity indices. However, it is important to note that the package does not include features for technical indicators or real-time trading. Active development is ongoing, with exciting new features planned for future releases. The goal of BharatFinTrack is to empower users by providing easy access to open-source data, enabling them to make informed financial decisions. Currently, the package offers the following features:


## [Nifty Indices](https://www.niftyindices.com/)
    
* Provides access to detailed information about NSE equity indices.
* Enables downloading and updating daily `Total Return Index (TRI)` data for all NSE equity indices.
* Fetches closing values for both `Price` (excluding dividend reinvestment) and `TRI` for all NSE equity indices.
    
## Functionality
    
* Calculates the updated Compound Annual Growth Rate (CAGR) for both `Price` and `TRI` since the inception of all NSE equity indices.
* Sorts NSE equity indices by CAGR (%) values.
* Sorts NSE equity indices by CAGR (%) within each category.


## Visualization

* Plots the descending CAGR (%) for NSE equity indices, organized by category since inception.
* Plots the top-performing NSE indices by CAGR (%) for a specified number of indices in each category since their launch.


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

# list of all NSE equity indices
>>> nse_product.all_equity_indices
['NIFTY 100',
 'NIFTY 200',
 'NIFTY 50',
 ...]
```

## Top Performing NSE Equity Indices

The bar plot displays the closing values for NSE equity indices `TRI` with the top five CAGR (%) since launch in each category.

![Top performing NSE equity indices by CAGR(%)](BharatFinTrack/data/tri_top_cagr_by_category.png)

## Documentation
For detailed information, see the [documentation](http://bharatfintrack.readthedocs.io/).

## Support

If this project has been helpful and you'd like to contribute to its development, consider sponsoring with a coffee! Support will help maintain, improve, and expand this open-source project, ensuring continued valuable tools for the community.


[![Buy Me a Coffee](https://img.shields.io/badge/☕_Buy_me_a_coffee-FFDD00?style=for-the-badge)](https://www.buymeacoffee.com/debasish_pal)


## Toolkit

| <big>Status</big> | <big>Description</big> |
| --- | --- |
| **PyPI**| ![PyPI - Version](https://img.shields.io/pypi/v/BharatFinTrack) ![PyPI - Status](https://img.shields.io/pypi/status/BharatFinTrack) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/BharatFinTrack) ![PyPI - Wheel](https://img.shields.io/pypi/wheel/BharatFinTrack) |
| **GitHub** | ![GitHub last commit](https://img.shields.io/github/last-commit/debpal/BharatFinTrack) [![flake8](https://github.com/debpal/BharatFinTrack/actions/workflows/linting.yml/badge.svg)](https://github.com/debpal/BharatFinTrack/actions/workflows/linting.yml)	[![mypy](https://github.com/debpal/BharatFinTrack/actions/workflows/typing.yml/badge.svg)](https://github.com/debpal/BharatFinTrack/actions/workflows/typing.yml) [![pytest](https://github.com/debpal/BharatFinTrack/actions/workflows/testing.yml/badge.svg)](https://github.com/debpal/BharatFinTrack/actions/workflows/testing.yml) |
| **Codecov** | [![codecov](https://codecov.io/github/debpal/BharatFinTrack/graph/badge.svg?token=6DIYX8MUTM)](https://codecov.io/github/debpal/BharatFinTrack) |
| **Read** _the_ **Docs** | [![Documentation Status](https://readthedocs.org/projects/bharatfintrack/badge/?version=latest)](https://bharatfintrack.readthedocs.io/en/latest/?badge=latest) |
| **PePy** | ![Pepy Total Downloads](https://img.shields.io/pepy/dt/BharatFinTrack) [![Downloads](https://static.pepy.tech/badge/BharatFinTrack/month)](https://pepy.tech/project/BharatFinTrack) |
| **License** | ![PyPI - License](https://img.shields.io/pypi/l/BharatFinTrack) |
