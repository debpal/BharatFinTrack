============
Quickstart
============

This guide provides a quick overview to get started with :mod:`BharatFinTrack`.


Verify Installation
---------------------
Ensure successful installation by running the following commands:

.. code-block:: python

    import BharatFinTrack
    nse_product = BharatFinTrack.NSEProduct()
    nse_index = BharatFinTrack.NSEIndex()
    nse_tri = BharatFinTrack.NSETRI()
    
    
NSE Equity Index Characteristics
----------------------------------


Category
^^^^^^^^^^

Retrieve the equity index categories:

.. code-block:: python

    nse_product.equity_index_category
    
Expected output:

.. code-block:: text

    ['broad', 'sector', 'thematic', 'strategy', 'variant']


Index List
^^^^^^^^^^^^^^

Get the list of all NSE equity indices:

.. code-block:: python
    
    nse_product.all_equity_indices
    
Expected output:

.. code-block:: text

    ['NIFTY 100',
     'NIFTY 200',
     'NIFTY 50',
     'NIFTY 50 ARBITRAGE',
     ...]


Categorical Index
^^^^^^^^^^^^^^^^^^^

Fetch equity indices belonging to a specific category:

.. code-block:: python
    
    nse_product.get_equity_indices_by_category('strategy')
    
Expected output:

.. code-block:: text

    ['NIFTY ALPHA 50',
     'NIFTY ALPHA LOW-VOLATILITY 30',
     'NIFTY ALPHA QUALITY LOW-VOLATILITY 30',
     'NIFTY ALPHA QUALITY VALUE LOW-VOLATILITY 30',
     ...]
     
     
Index Base Parameters
^^^^^^^^^^^^^^^^^^^^^^^

Retrieve the base date and base value of an equity index:

.. code-block:: python
    
    nse_product.get_equity_index_base_date('NIFTY 50')
    nse_product.get_equity_index_base_value('NIFTY 50')
    
Expected output:

.. code-block:: text

    '03-Nov-1995'
    1000.0
    
    
    
Download Data
---------------

NSE Indices Summary
^^^^^^^^^^^^^^^^^^^^^^^^^^
Download the daily summary report for all NSE indices, which is uploaded daily on the `Nifty Indices Reports <https://www.niftyindices.com/reports/daily-reports/>`_, and save
as 'daily_summary_report.csv' in the specified folder path.

.. code-block:: python

    nse_index.download_daily_summary_report(
        folder_path=r"C:\Users\Username\Folder"
    )


Total Return Index (TRI)
^^^^^^^^^^^^^^^^^^^^^^^^^^
Download historical daily TRI data, including both price and dividend reinvestment, for the NIFTY 50 index. 
Currently, the function supports only equity indices. 

.. code-block:: python
    
    # donwloading daily closing TRI data between start and end dates for NIFTY 50
    nse_tri.download_historical_daily_data(
        index='NIFTY 50',
    	start_date='01-Apr-2023',
    	end_date='31-Mar-2024',
        excel_file=r"C:\Users\Username\Folder\NIFTY50.xlsx"
    )
    
    # Using the same excel file to update daily closing TRI data to the present date
    nse_tri.update_historical_daily_dataa(
        index='NIFTY 50',
        excel_file=r"C:\Users\Username\Folder\NIFTY50.xlsx"
    )
