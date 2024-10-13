===============
Functionality
===============


A brief overview of several features related to making investment decisions.




Class Instance
----------------
Let's start by instantiating the classes.

.. code-block:: python

    import BharatFinTrack
    nse_index = BharatFinTrack.NSEIndex()
    nse_tri = BharatFinTrack.NSETRI()



.. _fucn_equity_index_price_cagr:

Equity Index Price CAGR
--------------------------

This functionality sorts the Compound Annual Growth Rate (CAGR) (%) of all NSE equity indices (excluding dividend reinvestment) from their inception and saves the results to an Excel file.
It helps users make informed decisions about investments in passive funds that track these indices.

.. code-block:: python

    nse_index.sort_equity_cagr_from_launch(
        excel_file=r"C:\Users\Username\Folder\sort_price_cagr.xlsx"
    )
    
    
Additionally, the sorting can be extended to keep equity index categories fixed. This allows users to 
better understand the difference in index returns across various categories


.. code-block:: python

    nse_index.category_sort_equity_cagr_from_launch(
        excel_file=r"C:\Users\Username\Folder\sort_price_cagr_by_category.xlsx"
    )
    

.. _fucn_equity_tri_cagr:

Equity TRI CAGR
------------------
Download the closing Total Return Index (TRI) values for all NSE indices. These values are not updated on the website on a daily basis. 
It is recommended to use this function at night when web traffic to the website is lower. The function sends several web requests to collect the required values.

.. code-block:: python
    
    excel_file = r"C:\Users\Username\Folder\tri_closing_value.xlsx"
    
    # equity indices closing value
    nse_tri.download_daily_summary_equity_closing(
        excel_file=excel_file
    )
    

The above Excel file will be used to sort the equity indices based on the CAGR (%) from their inception. This helps users understand the difference between actual CAGR (%) and TRI CAGR (%).
    
    
.. code-block:: python
    
    # sort equity indices by CAGR (%) since launch
    nse_tri.sort_equity_cagr_from_launch(
        input_excel=excel_file,
        output_excel=r"C:\Users\Username\Folder\sort_tri_cagr.xlsx"
    )
    
    # sort equity indices by CAGR (%) since launch within each category 
    nse_tri.category_sort_equity_cagr_from_launch(
        input_excel=excel_file,
        output_excel=r"C:\Users\Username\Folder\sort_tri_cagr_by_category.xlsx"
    )








    


    
    
