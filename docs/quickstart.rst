============
Quickstart
============

This guide provides a quick overview to get started with :mod:`BharatFinTrack`.


Verify Installation
---------------------
Ensure successful installation by running the following commands.

.. code-block:: python

    import BharatFinTrack
    nse_product = BharatFinTrack.NSEProduct()
    
    
Index Category
----------------

Retrieve the equity index categories.

.. code-block:: python

    nse_product.equity_index_category
    
Expected output:

.. code-block:: text

    ['broad', 'sector', 'thematic', 'strategy', 'variant']


Index List
-------------------

Get the list of all equity indices.

.. code-block:: python
    
    nse_product.all_equity_indices
    
Expected output:

.. code-block:: text

    ['NIFTY 100',
     'NIFTY 200',
     'NIFTY 50',
     ...]


Categorical Index
-------------------

Fetch equity indices belonging to a specific category.

.. code-block:: python
    
    nse_product.get_equity_indices_by_category('strategy')
    
Expected output:

.. code-block:: text

    ['NIFTY ALPHA 50',
     'NIFTY ALPHA LOW-VOLATILITY 30',
     'NIFTY ALPHA QUALITY LOW-VOLATILITY 30',
     ...]
     
     
Index Base Parameters
-----------------------

Retrieve the base date and base value of an equity index:

.. code-block:: python
    
    nse_product.get_equity_index_base_date('NIFTY 50')
    nse_product.get_equity_index_base_value('NIFTY 50')
    
Expected output:

.. code-block:: text

    '03-Nov-1995'
    1000.0
    
