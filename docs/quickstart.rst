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
^^^^^^^^^^^^^^^^

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

Total Return Index (TRI)
^^^^^^^^^^^^^^^^^^^^^^^^^^
Download historical daily TRI data, including both price and dividend reinvestment, for the NIFTY 50 index:

.. code-block:: python

    import BharatFinTrack
    nse_tri = BharatFinTrack.NSETRI()
    nse_tri.download_historical_daily_data(
        index='NIFTY 50',
    	start_date='23-Sep-2024',
    	end_date='27-Sep-2024'	
    )


Expected output:

.. code-block:: text

	      Date         Close
    0	2024-09-23	38505.51
    1	2024-09-24	38507.55
    2	2024-09-25	38602.21
    3	2024-09-26	38916.76
    4	2024-09-27	38861.64