# BharatFinTrack


![PyPI - Version](https://img.shields.io/pypi/v/BharatFinTrack) ![PyPI - Status](https://img.shields.io/pypi/status/BharatFinTrack) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/BharatFinTrack) ![PyPI - Wheel](https://img.shields.io/pypi/wheel/BharatFinTrack)

![GitHub last commit](https://img.shields.io/github/last-commit/debpal/BharatFinTrack) ![GitHub commit activity](https://img.shields.io/github/commit-activity/t/debpal/BharatFinTrack)
[![codecov](https://codecov.io/github/debpal/BharatFinTrack/graph/badge.svg?token=6DIYX8MUTM)](https://codecov.io/github/debpal/BharatFinTrack)


[![flake8](https://github.com/debpal/BharatFinTrack/actions/workflows/linting.yml/badge.svg)](https://github.com/debpal/BharatFinTrack/actions/workflows/linting.yml)	[![mypy](https://github.com/debpal/BharatFinTrack/actions/workflows/typing.yml/badge.svg)](https://github.com/debpal/BharatFinTrack/actions/workflows/typing.yml) [![pytest](https://github.com/debpal/BharatFinTrack/actions/workflows/testing.yml/badge.svg)](https://github.com/debpal/BharatFinTrack/actions/workflows/testing.yml)
![Read the Docs](https://img.shields.io/readthedocs/BharatFinTrack)


![GitHub Release Date](https://img.shields.io/github/release-date/debpal/BharatFinTrack)
![GitHub Created At](https://img.shields.io/github/created-at/debpal/BharatFinTrack)

![Pepy Total Downloads](https://img.shields.io/pepy/dt/BharatFinTrack)
![PyPI - License](https://img.shields.io/pypi/l/BharatFinTrack)



`BharatFinTrack` is a Python package designed to simplify the process of downloading and analyzing financial data from India. Conceptualized on September 1, 2024, and launched on September 8, 2024, the package is tailored for long-term investors looking to streamline their financial data workflows using reliable public sources. This package focuses on historical data and fundamental tracking; it does not include features for technical indicators or real-time trading. The package aims to empower users by providing easy access to open-source data, enabling them to make informed financial decisions. Currently, the package offers the following features:


## [Nifty Equity Indices](https://www.niftyindices.com/)
    
* Provides access to detailed information about equity indices.
* Enables downloading and updating daily Total Return Index (`TRI`) data for all equity indices.
* Fetches closing values for both Price Return Index (`PRI`), excluding dividend reinvestment, and `TRI` for all equity indices.


## [National Pension System](https://npstrust.org.in/weekly-snapshot-nps-schemes)
    
* Provides complete access to Pension Fund Manager (`PFM`) information alongside their respective schemes and unique identifiers.
* Enables downloading full historical Net Asset Value (`NAV`) data from inception for any given PFM and specified scheme.
* Fetches the most recent `NAV` values for selected schemes across multiple PFMs in a single workflow.


## Compound Annual Growth Rate (CAGR)
    
* Sorts `PRI` and `TRI` indices by CAGR (%) either globally or filtered within specific categories.
* Calculates year-wise CAGR rolling backward from the present date for a specified asset (either a `TRI` index or an `NPS` scheme).
* Compares the year-wise CAGR (%) and the compounding growth of a fixed annual investment across multiple assets (chosen from `TRI` indices or `NPS` schemes).

    
## Systematic Investment Plan (SIP)

* Estimates annual SIP performance, including investment amount, closing balance, and cumulative growth over a specified number of years and expected annual return, with options for yearly, quarterly, monthly, or weekly contributions.
* Calculates the terminal closing summary of an SIP with a fixed monthly contribution to a specified asset (either a `TRI` index or an `NPS` scheme) starting from a given date.
* Computes year-wise SIP returns rolling backward from the present date for a fixed monthly contribution, accepting either a specific `TRI` index or an `NPS` scheme as the asset.
* Compares the year-wise XIRR (%) and compounding growth of a fixed monthly SIP investment across multiple assets (chosen from `TRI` indices or `NPS` schemes).


## Analysis

* Identifies key turning points, peak-to-trough corrections, and recoveries over the historical timeline of an specified asset.
* Extracts historical values from downloaded data between the specified given start and end dates.


## Visualization

* Shows bar graphs of top-performing `PRI` and `TRI` indices by CAGR (%) since launch, with options to view a specified number of top indices, either overall or within each category.
* Compares returns between a specified index and government securities for a monthly SIP of 1 Rupee over time.
* Illustrates a line plot comparing the growth of a monthly SIP investment across multiple NSE equity `TRI` indices over the years.
* Depicts a line plot comparing the growth of a one-time investment across multiple NSE equity `TRI` indices over the years.


# Application
`BharatFinTrack` provides insights into the performance of equity indices. For instance, the following bar plot highlights the top five equity indices by `TRI` CAGR (%) within each category since their respective launches. This snapshot provides a powerful visual overview of long-term performance trends of CAGR (%) across different index categories over the years.

![Category-wise Top Five TRI CAGR(%) of NSE Equity Indices](https://github.com/debpal/BharatFinTrack/raw/main/docs/_static/sort_cagr_within_category.png)

In the above graph, the `NIFTY MIDCAP150 MOMENTUM 50` stands out as one of the best-performing NSE equity indices within the strategy category in terms of long-term CAGR (%). The following graph presents a comparison of year-wise investments and returns for a monthly SIP of 1 Rupee between government securities and a passive fund tracking the TRI of `NIFTY MIDCAP150 MOMENTUM 50`.

![Year-wise SIP comparison between NIFTY_MIDCAP150_MOMENTUM_50 and Government Bond](https://github.com/debpal/BharatFinTrack/raw/main/docs/_static/sip_growth_vs_bond_benchmark.png)

Additionally, the following plot compares the growth multiples (X) of a monthly SIP investment across `TRI` indices, including the popular index `NIFTY 50` and other top-performing NSE equity indices over the years.

![Year-wise SIP growth comparison across multiple indices](https://github.com/debpal/BharatFinTrack/raw/main/docs/_static/compare_sip.png)

## Installation

To install, use pip:

```bash
pip install BharatFinTrack
```

After a successful installation, the following code should run without errors:

```python
import BharatFinTrack
nse_product = BharatFinTrack.NSEProduct()
```

## Documentation
For detailed information, see the [documentation](https://bharatfintrack.readthedocs.io/en/latest/).

## Support

If this project has been helpful and you'd like to contribute to its development, consider sponsoring with a coffee! Support will help maintain, improve, and expand this open-source project, ensuring continued valuable tools for the community.


[![Buy Me a Coffee](https://img.shields.io/badge/☕_Buy_me_a_coffee-FFDD00?style=for-the-badge)](https://www.buymeacoffee.com/debasish_pal)
