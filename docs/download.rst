===============
Download Data
===============

A brief overview of the features related to downloading data.


Class Instance
----------------
Let's start by instantiating the classes.

.. code-block:: python

    import BharatFinTrack
    nse_index = BharatFinTrack.NSEIndex()
    nse_tri = BharatFinTrack.NSETRI()


NSE Indices Summary
---------------------

Download the daily summary report for all NSE indices, which is uploaded daily on the `Nifty Indices Reports <https://www.niftyindices.com/reports/daily-reports/>`_, and save
as 'summary_index_price_closing_value.csv' in the specified folder path.

.. code-block:: python

    nse_index.download_daily_summary_report(
        folder_path=r"C:\Users\Username\Folder"
    )



.. _f_download_tri:

Total Return Index (`TRI`)
----------------------------

Download historical daily `TRI` data, including both price and dividend reinvestment, for the NIFTY 50 index. 
Currently, the function supports only equity indices. 

.. code-block:: python
    
    # donwloading daily closing TRI data for NIFTY 50 up to a specified date
    nse_tri.download_historical_daily_data(
        index='NIFTY 50',
        excel_file=r"C:\Users\Username\Folder\NIFTY 50.xlsx",
    	start_date=None,
    	end_date='31-Mar-2024'   
    )
    
    # using the same excel file to update daily closing TRI data to the present date
    nse_tri.update_historical_daily_dataa(
        index='NIFTY 50',
        excel_file=r"C:\Users\Username\Folder\NIFTY 50.xlsx"
    )
