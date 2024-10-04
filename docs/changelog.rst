===============
Release Notes
===============


Version 0.1.2
--------------

* **Release date:** 04-Oct-2024
  
* **Changes:** 

    * Deprecated :meth:`BharatFinTrack.NSEIndex.all_equity_index_cagr_from_inception` and introduced :meth:`BharatFinTrack.NSEIndex.category_sort_equity_cagr_from_launch`.
    * Added functionality for sorting the CAGR (%) of all NSE equity indices from launch.
    * Introduced sorting of the CAGR (%) of NSE equity indices from launch while maintaining fixed index categories.

* **Development Status:** Upgraded from Alpha to Beta.


Version 0.1.1
--------------

* **Release date:** 02-Oct-2024

* **Feature Additions:** Introduced the :class:`BharatFinTrack.NSEIndex` class, which currently calculates the CAGR(%) of all NSE equity indices
  (excluding dividend reinvestment) from inception. Additional features are planned for future releases.

* **Documentation:** Updated to reflect the newly introduced features.

* **Development Status:** Upgraded from Pre-Alpha to Alpha.


Version 0.1.0
---------------

* **Release date:** 30-Sep-2024.

* **Feature Additions:** Introduced :class:`BharatFinTrack.NSETRI` class, which facilitates downloading Total Return Index (TRI) data for all NSE equity indices.
 
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