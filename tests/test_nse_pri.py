import pytest
import BharatFinTrack
import pandas
import tempfile
import os
import matplotlib.figure


@pytest.fixture(scope='class')
def nse_pri():

    yield BharatFinTrack.NSEPRI()


@pytest.fixture(scope='class')
def cagr():

    yield BharatFinTrack.CAGR()


@pytest.fixture(scope='class')
def analyzer():

    yield BharatFinTrack.Analyzer()


@pytest.fixture(scope='class')
def visual():

    yield BharatFinTrack.Visual()


def test_download_close_value(
    nse_pri,
    cagr,
    analyzer,
    visual
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
        df = cagr.sort_since_inception(
            csv_file=os.path.join(tmp_dir, 'PRI_daily_close.csv'),
            excel_file=os.path.join(tmp_dir, 'sort_cagr_within_category.xlsx'),
            within_category=True
        )
        assert isinstance(df, pandas.DataFrame)
        assert df.shape[1] == 8
        assert os.path.exists(os.path.join(tmp_dir, 'sort_cagr_within_category.xlsx'))

        # Pass test for sorting CAGR
        df = cagr.sort_since_inception(
            csv_file=os.path.join(tmp_dir, 'PRI_daily_close.csv'),
            excel_file=os.path.join(tmp_dir, 'sort_cagr.xlsx')
        )
        assert isinstance(df, pandas.DataFrame)
        assert df.shape[1] == 8
        assert os.path.exists(os.path.join(tmp_dir, 'sort_cagr.xlsx'))

        # Pass test of visual for CAGR leaders within category
        figure = visual.cagr_leaders_by_category(
            excel_file=os.path.join(tmp_dir, 'sort_cagr_within_category.xlsx'),
            figure_file=os.path.join(tmp_dir, 'sort_cagr_within_category.png'),
            fig_title='Sort CAGR within category',
            fig_ylabel='Index',
            gui_window=False
        )
        assert isinstance(figure, matplotlib.figure.Figure)
        assert os.path.exists(os.path.join(tmp_dir, 'sort_cagr_within_category.png'))

        # Pass test of visual for CAGR leaders
        figure = visual.cagr_leaders(
            excel_file=os.path.join(tmp_dir, 'sort_cagr.xlsx'),
            figure_file=os.path.join(tmp_dir, 'sort_cagr.png'),
            fig_title='Sort CAGR',
            fig_ylabel='Index',
            gui_window=False
        )
        assert isinstance(figure, matplotlib.figure.Figure)
        assert os.path.exists(os.path.join(tmp_dir, 'sort_cagr.png'))
