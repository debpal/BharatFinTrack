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

    import BharatFinTrack
    nse_index = BharatFinTrack.NSEIndex()
    nse_index.sort_equity_cagr_from_launch(
        excel_file=r"C:\Users\Username\Folder\sort_cagr.xlsx"
    )
    
    
Additionally, the sorting can be extended to keep equity index categories fixed. This allows users to focus on specific passive fund categories and 
better understand the difference in index returns across various categories.


.. code-block:: python

    nse_index.category_sort_equity_cagr_from_launch(
        excel_file=r"C:\Users\Username\Folder\category_sort_cagr.xlsx"
    )








    


    
    
