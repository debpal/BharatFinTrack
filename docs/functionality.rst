===============
Functionality
===============
    
    
Compound Annual Growth Rate (CAGR)
-------------------------------------

Equity Index Price from Launch
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This functionality sorts the CAGR (%) of all NSE equity indices (excluding dividend reinvestment) from their inception and saves the results to an Excel file. 
This feature helps users make informed decisions about investments in passive funds that track these indices.

.. code-block:: python

    nse_index.sort_equity_cagr_from_launch(
        excel_file=r"C:\Users\Username\Folder\sort_cagr.xlsx"
    )
    
    
Additionally, the sorting can be extended to keep equity index categories fixed. This allows users to focus on specific passive fund categories and 
better understand the difference in index returns across various categories.


.. code-block:: python

    nse_index.category_sort_equity_cagr_from_launch(
        excel_file=r"C:\Users\Username\Folder\category_sort_cagr.xlsx"
    )
    
    
Equity Total Return Index (TRI) Summary
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Download the closing TRI values for all NSE indices. These values are not updated on the website on a daily basis. 
It is recommended to use this function at night when web traffic to the website is lower. The function sends several web requests to collect the required values.

.. code-block:: python
    
    excel_file = r"C:\Users\Username\Folder\tri_closing_value.xlsx"
    
    # equity indices closing value
    nse_tri.download_daily_summary_equity_closing(
        excel_file=excel_file
    )
    
    # sort equity indices by closing value
    nse_tri.sort_equity_value_from_launch(
        input_excel=excel_file,
        output_excel=r"C:\Users\Username\Folder\sorted_tri_value.xlsx"
    )
    
    # sort equity indices by CAGR (%) since launch
    nse_tri.sort_equity_cagr_from_launch(
        input_excel=excel_file,
        output_excel=r"C:\Users\Username\Folder\sorted_tri_cagr.xlsx"
    )
    
    # sort equity indices by CAGR (%) since launch within each category 
    nse_tri.category_sort_equity_cagr_from_launch(
        input_excel=excel_file,
        output_excel=r"C:\Users\Username\Folder\category_sort_tri_cagr.xlsx"
    )








    


    
    
