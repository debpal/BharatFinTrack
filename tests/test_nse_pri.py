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


@pytest.fixture(scope='class')
def analyzer():

    yield BharatFinTrack.Analyzer()


def test_download_equity_index_close(
    nse_pri,
    cagr,
    analyzer
):

    with tempfile.TemporaryDirectory() as tmp_dir:

        # Pass test for downloading daily closing value
        df = nse_pri.download_equity_close(
            csv_file=os.path.join(tmp_dir, 'PRI_daily_close.csv'),
            untracked_base_equity=True
        )
        assert isinstance(df, pandas.DataFrame)
        assert df.shape[1] == 7
        assert os.path.exists(os.path.join(tmp_dir, 'PRI_daily_close.csv'))

        # Pass test for sorting closing value
        df = analyzer.sort_equity_index_close(
            csv_file=os.path.join(tmp_dir, 'PRI_daily_close.csv'),
            excel_file=os.path.join(tmp_dir, 'sort_closing.xlsx')
        )
        assert isinstance(df, pandas.DataFrame)
        assert df.shape[1] == 6
        assert os.path.exists(os.path.join(tmp_dir, 'sort_closing.xlsx'))

        # Pass test for sorting CAGR within category
        df = cagr.sort_indices_since_launch(
            csv_file=os.path.join(tmp_dir, 'PRI_daily_close.csv'),
            excel_file=os.path.join(tmp_dir, 'sort_cagr_within_category.xlsx'),
            within_category=True
        )
        assert isinstance(df, pandas.DataFrame)
        assert df.shape[1] == 8
        assert os.path.exists(os.path.join(tmp_dir, 'sort_cagr_within_category.xlsx'))
