===============
Release Notes
===============

Version 0.1.8
---------------

* **Release date:** 01-Nov-2024
  
* **Feature Additions:** 

    * Enhanced functionality for SIP in the :class:`BharatFinTrack.NSETRI` class.
    * Added data visualization capabilities for SIP in the :class:`BharatFinTrack.Visual` class.


Version 0.1.7
---------------

* **Release date:** 26-Oct-2024
  
* **Feature Additions:** 

    * Added support for newly launched NSE equity indices.
    * Enhanced functionality for calculating the CAGR difference between `Price` and `TRI` indices in the :class:`BharatFinTrack.NSETRI` class.
    * Improved data visualization capabilities in the :class:`BharatFinTrack.Visual` class.


Version 0.1.6
---------------

* **Release date:** 24-Oct-2024
  
* **Feature Additions:** 

    * Added new equity indices launched by NSE.
    * Enhanced functionality for data visualization in the :class:`BharatFinTrack.Visual` class.


Version 0.1.5
---------------

* **Release date:** 13-Oct-2024
  
* **Feature Additions:**

    * Introduced the :class:`BharatFinTrack.Visual` class for data visualization.
    * Added the :meth:`BharatFinTrack.Visual.plot_category_sort_index_cagr_from_launch` method for plotting the descending sort of CAGR (%) by index category since inception.


Version 0.1.4
---------------

* **Release date:** 09-Oct-2024
  
* **Feature Additions:** Updates the pre-downloaded Excel file of daily Total Return Index data for a specified index from the last date to the present.
    
* **Changes:** Deprecated :meth:`BharatFinTrack.NSETRI.download_equity_indices_updated_value` and renamed :meth:`BharatFinTrack.NSETRI.download_daily_summary_equity_closing`.


Version 0.1.3
---------------

* **Release date:** 06-Oct-2024
  
* **Feature Additions:**
    
    * Fetches updated Total Return Index values for all NSE equity indices.
    * Sorts the CAGR (%) of all NSE equity TRI values since launch.

* **Bug Fixes:** Issues with the API used to fetch Total Return Index data.

* **Development Status:** Upgraded from Alpha to Beta.


Version 0.1.2
---------------

* **Release date:** 04-Oct-2024
  
* **Changes:** Deprecated :meth:`BharatFinTrack.NSEIndex.all_equity_index_cagr_from_inception`.
    
* **Feature Additions:** Added functionality for sorting the CAGR (%) of all NSE equity index prices since launch.


Version 0.1.1
---------------

* **Release date:** 02-Oct-2024

* **Feature Additions:** Introduced the :class:`BharatFinTrack.NSEIndex` class, which currently calculates the CAGR(%) of all NSE equity indices
  (excluding dividend reinvestment) from inception. Additional features are planned for future releases.

* **Documentation:** Updated to reflect the newly introduced features.

* **Development Status:** Upgraded from Pre-Alpha to Alpha.


Version 0.1.0
---------------

* **Release date:** 30-Sep-2024.

* **Feature Additions:** Introduced :class:`BharatFinTrack.NSETRI` class, which facilitates downloading Total Return Index data for all NSE equity indices.
 
* **Changes:** 

    * Renamed class :class:`BharatFinTrack.NSETrack` to :class:`BharatFinTrack.NSEProduct` for improved clarity.
    * Updated and renamed methods in the new class :class:`BharatFinTrack.NSEProduct`.

* **Documentation:** Added a tutorial on how to use the newly introduced features.

* **Development status:** Upgraded from Planning to Pre-Alpha.


Version 0.0.3
---------------

* **Release date:** 11-Sep-2024.

* **GitHub Actions Integration:**

    * Linting with `flake8` to enforce PEP8 code formatting.
    * Type checking with `mypy` to verify annotations throughout the codebase.
    * Testing with `pytest` to run tests and ensure code reliability.
    * Test Coverage with **Codecov** to monitor and report test coverage.
    
* **Compatibity:** Verified compatibility with Python 3.10, 3.11, and 3.12.

* **Documentation:** Added new badges to `README.md` to display statuses of linting, type-checking, testing, and coverage.


Version 0.0.2
---------------

* **Release date:** 09-Sep-2024.

* **Bug Fixes:** Some bug fixes.

* **Documentation:** Updated `README.md`.


Version 0.0.1
---------------

* **Release date:** 08-Sep-2024.

* **Features:** Functionality for accessing the characteristics of NSE equity Indices.

* **Development status:** Planning.

* **Roadmap:** Ongoing addition of new features.