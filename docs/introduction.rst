==============
Introduction
==============

:mod:`BharatFinTrack` is a Python package designed to simplify the process of downloading and analyzing financial data from India. Conceptualized on September 1, 2024, and launched on September 8, 2024, the package is tailored for long-term investors looking to streamline their financial data workflows using reliable public sources. This package focuses on historical data and fundamental tracking; it does not include features for technical indicators or real-time trading. The package aims to empower users by providing easy access to open-source data, enabling them to make informed financial decisions. Currently, the package offers the following features:


`Nifty Equity Indices <https://www.niftyindices.com/>`_
------------------------------------------------------------------------------------
    
* Provides access to detailed information about equity indices.
* Enables downloading and updating daily Total Return Index (``TRI``) data for all equity indices.
* Fetches closing values for both Price Return Index (``PRI``), excluding dividend reinvestment, and ``TRI`` for all equity indices.


`National Pension System <https://npstrust.org.in/weekly-snapshot-nps-schemes>`_
------------------------------------------------------------------------------------
    
* Provides complete access to Pension Fund Manager (``PFM``) information alongside their respective schemes and unique identifiers.
* Enables downloading full historical Net Asset Value (``NAV``) data from inception for any given PFM and specified scheme.
* Fetches the most recent ``NAV`` values for selected schemes across multiple PFMs in a single workflow.
    
    
Compound Annual Growth Rate (CAGR)
----------------------------------------

* Sorts ``PRI`` and ``TRI`` indices by CAGR (%) either globally or filtered within specific categories.
* Calculates year-wise CAGR rolling backward from the present date for a specified asset (either a ``TRI`` index or an ``NPS`` scheme).
* Compares the year-wise CAGR (%) and the compounding growth of a fixed annual investment across multiple assets (chosen from ``TRI`` indices or ``NPS`` schemes).


Systematic Investment Plan (SIP)
----------------------------------

* Estimates annual SIP performance, including investment amount, closing balance, and cumulative growth over a specified number of years and expected annual return, with options for yearly, quarterly, monthly, or weekly contributions.
* Calculates the terminal closing summary of an SIP with a fixed monthly contribution to a specified asset (either a ``TRI`` index or an ``NPS`` scheme) starting from a given date.
* Computes year-wise SIP returns rolling backward from the present date for a fixed monthly contribution, accepting either a specific ``TRI`` index or an ``NPS`` scheme as the asset.
* Compares the year-wise XIRR (%) and compounding growth of a fixed monthly SIP investment across multiple assets (chosen from ``TRI`` indices or ``NPS`` schemes).


Analysis
-----------

* Identifies key turning points, peak-to-trough corrections, and recoveries over the historical timeline of an specified asset.
* Extracts historical values from downloaded data between the specified given start and end dates.


Visualization
---------------

* Shows bar graphs of top-performing ``PRI`` and ``TRI`` indices by CAGR (%) since launch, with options to view a specified number of top indices, either overall or within each category.
* Compares returns between a specified index and government securities for a monthly SIP of 1 Rupee over time.
* Illustrates a line plot comparing the growth of a monthly SIP investment across multiple NSE equity ``TRI`` indices over the years.
* Depicts a line plot comparing the growth of a one-time investment across multiple NSE equity ``TRI`` indices over the years.
    