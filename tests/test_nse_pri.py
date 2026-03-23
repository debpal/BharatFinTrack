import pytest
import BharatFinTrack
import pandas
import tempfile
import os


@pytest.fixture(scope='class')
def nse_pri():

    yield BharatFinTrack.NSEPRI()


@pytest.fixture(scope='class')
def cagr():

    yield BharatFinTrack.CAGR()


def test_equity_index_price_download_updated_value(
    nse_pri,
    cagr
):

    with tempfile.TemporaryDirectory() as tmp_dir:

        # Pass test for downloading daily closing value
        close_df = nse_pri.download_equity_close(
            csv_file=os.path.join(tmp_dir, 'PRI_daily_close.csv'),
            untracked_base_equity=True
        )
        assert isinstance(close_df, pandas.DataFrame)
        assert close_df.shape[1] == 7
        assert os.path.exists(os.path.join(tmp_dir, 'PRI_daily_close.csv'))

        # Pass test for sorting CAGR within category
        cagr_df = cagr.sort_indices_since_launch(
            csv_file=os.path.join(tmp_dir, 'PRI_daily_close.csv'),
            excel_file=os.path.join(tmp_dir, 'sort_cagr_within_category.xlsx'),
            within_category=True
        )
        assert isinstance(cagr_df, pandas.DataFrame)
        assert cagr_df.shape[1] == 8
        assert os.path.exists(os.path.join(tmp_dir, 'sort_cagr_within_category.xlsx'))
