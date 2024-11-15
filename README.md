# BharatFinTrack


`BharatFinTrack` is a Python package designed to simplify the process of downloading and analyzing financial data from India. Conceptualized on September 1, 2024, and launched on September 8, 2024, this package is tailored for long-term investors seeking to streamline their financial data workflows. 

`BharatFinTrack` focuses on open-source financial data, with an initial emphasis on analyzing NSE equity indices. However, it is important to note that the package does not include features for technical indicators or real-time trading. Active development is ongoing, with exciting new features planned for future releases. The goal of BharatFinTrack is to empower users by providing easy access to open-source data, enabling them to make informed financial decisions. Currently, the package offers the following features:


## [Nifty Indices](https://www.niftyindices.com/)
    
* Provides access to detailed information about NSE equity indices.
* Enables downloading and updating daily (`TRI`) data for all NSE equity indices.
* Fetches closing values for both `Price` (excluding dividend reinvestment) and `TRI` for all NSE equity indices.

## Compound Annual Growth Rate (CAGR)
    
* Calculates CAGR for both `Price` and `TRI` since the inception of all NSE equity indices.
* Compare CAGR (%) between `Price` and `TRI`.
* Sorts NSE equity indices by CAGR (%) values.
* Sorts NSE equity indices by CAGR (%) within each category.
    
## Systematic Investment Plan (SIP)
    
* Computes the year-wise SIP return for a fixed monthly contribution to a specified NSE equity `TRI` index. 
* Calculates the closing summary of an SIP with a fixed monthly contribution to a specified NSE equity `TRI` index, starting from a given date.
* Compares the growth of a monthly SIP investment across multiple NSE equity `TRI` indices over the years.
* Estimates annual SIP performance, including investment amount, closing balance, and cumulative growth over a specified number of years and expected annual return, with options for yearly, quarterly, monthly, or weekly contributions.


## Visualization

* Displays bar graphs of NSE equity indices’ closing values with descending CAGR (%) since inception, both overall and by index category.
* Shows bar graphs of top-performing NSE equity indices by CAGR (%) since launch, with options to view a specified number of top indices, either overall or within each category.
* Depicts a bar graph of year-wise investments and returns for a monthly SIP of 1,000 Rupees in a specified NSE equity `TRI` index since its inception.
* Provides a return comparison between a specified index and government bonds for a monthly SIP of 1,000 Rupees over the years.
* Illustrates a line plot comparing the growth of a monthly SIP investment across multiple NSE equity `TRI` indices over the years.


# Example Insights
Using `BharatFinTrack`, you can quickly gain insights into the performance of NSE equity indices. For instance, the following bar plot highlights the top five NSE equity indices by `TRI` CAGR (%) within each category since their respective launches. This snapshot provides a powerful visual overview of long-term performance trends of investment multiples (X) across different index categories over the years. Because performance data updates daily with each trading session, you can replicate and customize this analysis to generate up-to-date insights tailored to your research needs or investment strategies.

![Category-wise Top Five TRI CAGR(%) of NSE Equity Indices](https://github.com/debpal/BharatFinTrack/raw/master/docs/_static/tri_top_cagr_by_category.png)

In this graph, the `NIFTY MIDCAP150 MOMENTUM 50` stands out as one of the best-performing NSE equity `TRI` indices in terms of long-term CAGR. The next graph illustrates the year-wise investments and returns, shown as investment multiples (X) and XIRR (%), for a monthly SIP of 1,000 Rupees in a passive fund tracking the `TRI` data of `NIFTY MIDCAP150 MOMENTUM 50`.


![Year-wise SIP analysis of NIFTY_MIDCAP150_MOMENTUM_50](https://github.com/debpal/BharatFinTrack/raw/master/docs/_static/sip_yearwise_NIFTY_MIDCAP150_MOMENTUM_50.png)

Additionally, the following plot compares the growth multiples (X) of a monthly SIP investment across `TRI` indices, including popular indices such as `NIFTY 50` and `NIFTY 500`, as well as several other top-performing NSE equity indices over the years.


![Year-wise SIP growth comparison across multiple indices](https://github.com/debpal/BharatFinTrack/raw/master/docs/_static/sip_invest_growth_across_indices.png)

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
| **PePy** | ![Pepy Total Downloads](https://img.shields.io/pepy/dt/BharatFinTrack)|
| **License** | ![PyPI - License](https://img.shields.io/pypi/l/BharatFinTrack) |
