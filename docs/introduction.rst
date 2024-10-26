==============
Introduction
==============

`BharatFinTrack` is a Python package designed to simplify the process of downloading and analyzing financial data from India. Conceptualized on September 1, 2024, and launched on September 8, 2024, this package is tailored for long-term investors seeking to streamline their financial data workflows. 

`BharatFinTrack` focuses on open-source financial data, with an initial emphasis on analyzing NSE equity indices. However, it is important to note that the package does not include features for technical indicators or real-time trading. Active development is ongoing, with exciting new features planned for future releases. The goal of BharatFinTrack is to empower users by providing easy access to open-source data, enabling them to make informed financial decisions. Currently, the package offers the following features:


`Nifty Indices <https://www.niftyindices.com/>`_
---------------------------------------------------

* Provides access to detailed information about NSE equity indices.
* Enables downloading and updating daily `Total Return Index (TRI)` data for all NSE equity indices.
* Fetches closing values for both `Price` (excluding dividend reinvestment) and TRI for all NSE equity indices.
    
    
Functionality
---------------


* Calculates the updated Compound Annual Growth Rate (CAGR) for both `Price` and `TRI` since the inception of all NSE equity indices.
* Sorts NSE equity indices by CAGR (%) values.
* Sorts NSE equity indices by CAGR (%) within each category.


Visualization
---------------

* Displays bar graphs of NSE equity indices’ closing values with descending CAGR (%) since inception, both overall and by index category.
* Shows bar graphs of top-performing NSE equity indices by CAGR (%) since launch, with options to view a specified number of top indices, either overall or within each category.
    