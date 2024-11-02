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
    core = BharatFinTrack.core.Core()



.. _f_equity_index_price_cagr:

Equity Index `Price` CAGR
--------------------------

This functionality sorts the CAGR of the closing `Price` for all NSE equity indices from their inception and saves the results to an Excel file. 
It enables users to make informed decisions about investments in passive funds that track these indices.

.. code-block:: python

    nse_index.sort_equity_cagr_from_launch(
        excel_file=r"C:\Users\Username\Folder\price_sort_cagr.xlsx"
    )
    
    
Additionally, the sorting can be extended to keep equity index categories fixed. This allows users to 
better understand the difference in index returns across various categories


.. code-block:: python

    nse_index.category_sort_equity_cagr_from_launch(
        excel_file=r"C:\Users\Username\Folder\price_sort_cagr_by_category.xlsx"
    )
    

.. _f_equity_tri_cagr:

Equity `TRI` CAGR
------------------
Download the closing `TRI` values for all NSE indices. These values are not updated on the website on a daily basis. 
It is recommended to use this function at night when web traffic to the website is lower. The function sends several web requests to collect the required values.

.. code-block:: python
    
    excel_file = r"C:\Users\Username\Folder\summary_index_tri_closing_value.xlsx"
    
    # equity indices closing value
    nse_tri.download_daily_summary_equity_closing(
        excel_file=excel_file
    )
    
    
The above Excel file is used to sort equity indices based on their CAGR since inception. 
    
.. code-block:: python
    
    # sort equity indices by CAGR (%) since launch
    nse_tri.sort_equity_cagr_from_launch(
        input_excel=excel_file,
        output_excel=r"C:\Users\Username\Folder\tri_sort_cagr.xlsx"
    )
    
    # sort equity indices by CAGR (%) since launch within each category 
    nse_tri.category_sort_equity_cagr_from_launch(
        input_excel=excel_file,
        output_excel=r"C:\Users\Username\Folder\tri_sort_cagr_by_category.xlsx"
    )
    
    
CAGR Difference
-----------------
This method shows users the differences in CAGR between the `Price` and `TRI` of NSE equity indices.

.. code-block:: python
    
    nse_tri.compare_cagr_over_price(
        tri_excel=r"C:\Users\Username\Folder\tri_sort_cagr.xlsx",
        price_excel=r"C:\Users\Username\Folder\price_sort_cagr.xlsx"
        output_excel=r"C:\Users\Username\Folder\compare_cagr_tri_price.xlsx"
    )
    
    
SIP Growth
------------
Computes the year-wise SIP return for a fixed monthly contribution to a specified NSE equity `TRI` index. The data required to compute the SIP must be sourced from the Excel file generated in the :ref:`Total Return Index (TRI) <f_download_tri>` section. 


.. code-block:: python
    
    nse_tri.yearwise_sip_analysis(
        input_excel=r"C:\Users\Username\Folder\NIFTY 50.xlsx",
        monthly_invest=1000,
        output_excel=r"C:\Users\Username\Folder\SIP_Yearwise_NIFTY_50.xlsx"
    )
   
   
SIP Calculator
----------------
Estimates the SIP growth over a specified number of years for a fixed investment amount.


.. code-block:: python
    
    core.sip_growth(
        invest=1000,
        frequency='monthly',
        annual_return=15,
        years=20
    )
    
