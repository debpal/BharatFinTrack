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
        csv_file=r"C:\Users\Username\Folder\summary_index_price_closing_value.csv",
        excel_file=r"C:\Users\Username\Folder\price_sort_cagr.xlsx"
    )
    
    
Additionally, the sorting can be extended to keep equity index categories fixed. This allows users to 
better understand the difference in index returns across various categories


.. code-block:: python

    nse_index.category_sort_equity_cagr_from_launch(
        csv_file=r"C:\Users\Username\Folder\summary_index_price_closing_value.csv",
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
    
    
Year-wise SIP Growth
----------------------
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
    
    
Year-wise SIP and CAGR Comparison Across Indices
--------------------------------------------------
This section compares the year-wise XIRR (%) and growth multiples (X) of a fixed monthly SIP investment, along with the year-wise CAGR (%) and growth multiples of a fixed yearly investment across selected `TRI` indices, including the popular `NIFTY 50` and other top-performing NSE equity indices.

The required data are sourced from Excel files generated in the :ref:`Total Return Index (TRI) <f_download_tri>` section. Ensure that all input Excel files are stored in the designated folder, with each file named as `{index}.xlsx` to correspond to the index names provided in the list. The output highlights the highest growth cells in green-yellow and the lowest growth cells in sandy brown.

.. code-block:: python

    index_list = [
        'NIFTY 50',
        'NIFTY ALPHA 50',
        'NIFTY MIDCAP150 MOMENTUM 50',
        'NIFTY500 MOMENTUM 50'
    ]
    
    nse_tri.yearwise_sip_xirr_growth_comparison_across_indices(
        indices=index_list
        folder_path=r"C:\Users\Username\Folder",
        excel_file=r"C:\Users\Username\Folder\yearwise_sip_xirr_growth_across_indices.xlsx"
    )
    
    nse_tri.yearwise_cagr_growth_comparison_across_indices(
        indices=index_list
        folder_path=r"C:\Users\Username\Folder",
        excel_file=r"C:\Users\Username\Folder\yearwise_cagr_growth_across_indices.xlsx"
    )
    
    

Index Correction and Recovery
---------------------------------

This functionality identifies key turning points in an index's history based on consecutive corrections and recoveries.
It applies minimum gain and multiplier filters to analyze the frequency and behavior of these movements over time. 
The required data is sourced from the :ref:`Total Return Index (TRI) <f_download_tri>` section.

Test


.. code-block:: python

    nse_index.analyze_correction_recovery(
        input_excel=r"C:\Users\Username\Folder\NIFTY 50.xlsx",
        output_excel=r"C:\Users\Username\Folder\price_sort_cagr.xlsx",
        minimum_gain=10,
        multiplier_correction=2.5,
        multiplier_recovery=10
    )