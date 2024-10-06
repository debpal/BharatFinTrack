==============
Introduction
==============

BharatFinTrack is a Python package designed to simplify the process of downloading and analyzing financial data from India. Conceptualized on September 1, 2024, and launched on September 8, 2024, this package is tailored for long-term investors seeking to streamline their financial data workflows. It focuses on open-source financial data and currently provides functionality for analyzing NSE equity indices. However, it is important to note that the package does not include features for technical indicators or real-time trading at this time. Active development is ongoing, with exciting new features planned for future releases. The goal of BharatFinTrack is to empower users by offering easy access to open-source data, enabling them to make informed financial decisions. Currently, the package offers the following features:


* `Nifty Indices <https://www.niftyindices.com/>`_

    - Provides access to the characteristics of NSE equity indices.
    - Fetches updated values of prices (excluding dividend reinvestment) and Total Return Index (TRI) for all NSE equity indices.
    - Facilitates downloading TRI data for all NSE equity indices between the specified start and end dates, inclusive.
    
    
* Analysis
    
    - Calculates the updated CAGR (%) of all NSE equity index prices and TRI since their inception.
    - Sorts equity indices by CAGR (%) values since inception.
    