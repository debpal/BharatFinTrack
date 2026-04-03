==============
Introduction
==============

:mod:`BharatFinTrack` is a Python package designed to simplify the process of downloading and analyzing financial data from India. Conceptualized on September 1, 2024, and launched on September 8, 2024, this package is tailored for long-term investors seeking to streamline their financial data workflows. The package focuses on open-source financial data, with an initial emphasis on analyzing `Nifty Equity Indices <https://www.niftyindices.com/>`_. However, it is important to note that the package does not include features for technical indicators or real-time trading. Active development is ongoing, with exciting new features planned for future releases. The package aims is to empower users by providing easy access to open-source data, enabling them to make informed financial decisions. Currently, the package offers the following features:


Nifty Equity Indices
--------------------------

* Provides access to detailed information about equity indices.
* Enables downloading and updating daily Total Return Index (``TRI``) data for all equity indices.
* Fetches closing values for both Price Return Index (``PRI``), excluding dividend reinvestment, and ``TRI`` for all equity indices.
* Identifies key turning points in consecutive corrections and recoveries over the historical values of an index.
    
    
Compound Annual Growth Rate (CAGR)
----------------------------------------

* Calculates CAGR for both ``PRI`` and ``TRI`` indices since the inception.
* Sorts ``PRI`` and ``TRI`` indices by CAGR (%) either overall or within each category.
* Compares the year-wise CAGR (%) and growth of a fixed yearly investment across multiple ``TRI`` indices.


Systematic Investment Plan (SIP)
----------------------------------

* Computes the year-wise SIP return for a fixed monthly contribution to a specified ``TRI`` index. 
* Calculates the closing summary of an SIP with a fixed monthly contribution to a specified ``TRI`` index, starting from a given date.
* Compares the year-wise XIRR (%) and growth of a fixed monthly SIP investment across multiple ``TRI`` indices.
* Estimates annual SIP performance, including investment amount, closing balance, and cumulative growth over a specified number of years and expected annual return, with options for yearly, quarterly, monthly, or weekly contributions.


Visualization
---------------

* Shows bar graphs of top-performing ``PRI`` and ``TRI`` indices by CAGR (%) since launch, with options to view a specified number of top indices, either overall or within each category.
* Compares returns between a specified index and government securities for a monthly SIP of 1 Rupee over time.
* Illustrates a line plot comparing the growth of a monthly SIP investment across multiple NSE equity ``TRI`` indices over the years.
* Depicts a line plot comparing the growth of a one-time investment across multiple NSE equity ``TRI`` indices over the years.
    