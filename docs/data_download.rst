==================
Downloading Data
==================

A brief overview of the features for downloading data.
    
    
Total Return Index Data
-------------------------
Download historical daily data for the NIFTY 50 index:

.. code-block:: python

    import BharatFinTrack
    nse_tri = BharatFinTrack.NSETRI()
    nse_tri.download_historical_daily_data(
        index='NIFTY 50',
    	start_date='23-SEP-2024',
    	end_date='27-SEP-2024'	
    )


Expected output:

.. code-block:: text

	      Date         Close
    -----------------------------
    0	2024-09-23	38505.51
    1	2024-09-24	38507.55
    2	2024-09-25	38602.21
    3	2024-09-26	38916.76
    4	2024-09-27	38861.64







    


    
    
