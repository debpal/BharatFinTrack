import pytest
import BharatFinTrack
import pandas
import tempfile
import os


@pytest.fixture(scope='class')
def nse_index():

    yield BharatFinTrack.NSEIndex()


def test_equity_index_price_download_updated_value(
    nse_index,
    capsys
):

    with tempfile.TemporaryDirectory() as tmp_dir:
        # pass test for downloading daily summary report
        nse_index.download_daily_summary_report(
            folder_path=tmp_dir
        )
        # pass test for capturing print statement
        csv_file = os.path.join(tmp_dir, "summary_index_price_closing_value.csv")
        nse_index.equity_cagr_from_launch(
            csv_file=csv_file,
            untracked_indices=True
        )
        capture_print = capsys.readouterr()
        assert 'List of untracked download indices' in capture_print.out
        assert 'List of untracked base indices' in capture_print.out
        # pass test for sorting of NSE equity indices by CAGR (%) value
        nse_index.sort_equity_cagr_from_launch(
            csv_file=csv_file,
            excel_file=os.path.join(tmp_dir, 'index_sort_cagr.xlsx')
        )
        df = pandas.read_excel(
            io=os.path.join(tmp_dir, 'index_sort_cagr.xlsx')
        )
        assert len(df.index.names) == 1
        # pass test for categorical sorting NSE equity indices by CAGR (%) value
        nse_index.category_sort_equity_cagr_from_launch(
            csv_file=csv_file,
            excel_file=os.path.join(tmp_dir, 'index_category_sort_cagr.xlsx')
        )
        df = pandas.read_excel(
            io=os.path.join(tmp_dir, 'index_category_sort_cagr.xlsx'),
            index_col=[0, 1]
        )
        assert df.shape[1] == 9
        assert len(df.index.get_level_values('Category').unique()) <= 5

    # error test for folder path
    with tempfile.TemporaryDirectory() as tmp_dir:
        pass
    with pytest.raises(Exception) as exc_info:
        nse_index.download_daily_summary_report(tmp_dir)
    assert exc_info.value.args[0] == 'The folder path does not exist.'
