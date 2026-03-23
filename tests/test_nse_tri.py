import pytest
import BharatFinTrack
import os
import tempfile
import pandas


@pytest.fixture(scope='class')
def nse_tri():

    yield BharatFinTrack.NSETRI()


@pytest.fixture(scope='class')
def helper():

    yield BharatFinTrack.helper.Helper()


@pytest.fixture(scope='class')
def cagr():

    yield BharatFinTrack.CAGR()


@pytest.fixture(scope='class')
def sip():

    yield BharatFinTrack.SIP()


@pytest.fixture(scope='class')
def analyzer():

    yield BharatFinTrack.Analyzer()


def test_download(
    nse_tri,
    cagr,
    sip,
    analyzer,
    helper
):

    with tempfile.TemporaryDirectory() as tmp_dir:

        # Pass test for download daily data of index
        index = 'NIFTY ALPHA 50'
        daily_df = nse_tri.download_daily_data(
            index=index,
            start_date='01-Jan-2021',
            end_date='31-Dec-2025',
            csv_file=os.path.join(tmp_dir, f'{index}.csv')
        )
        assert isinstance(daily_df, pandas.DataFrame)
        assert len(daily_df) > 0
        assert daily_df['Date'].iloc[-1].strftime(helper._date_str_fmt) == '31-Dec-2025'
        assert int(daily_df['Close'].iloc[-1]) == 61247
        assert os.path.exists(os.path.join(tmp_dir, f'{index}.csv'))

        # Pass test for updation of downloaded daily data
        update_df = nse_tri.update_daily_data(
            index=index,
            csv_file=os.path.join(tmp_dir, f'{index}.csv')
        )
        assert isinstance(update_df, pandas.DataFrame)
        assert len(update_df) > 0
        assert update_df['Date'].iloc[0].strftime(helper._date_str_fmt) == '31-Dec-2025'
        assert int(update_df['Close'].iloc[0]) == 61247

        # Pass test for extraction of downloaded daily data
        extract_df = analyzer.extract_data_between_dates(
            input_csv=os.path.join(tmp_dir, f'{index}.csv'),
            start_date='01-Jun-2025',
            end_date='01-Aug-2025',
            output_csv=os.path.join(tmp_dir, f'{index}_extract.csv')
        )
        assert isinstance(extract_df, pandas.DataFrame)
        assert len(extract_df) > 0
        assert extract_df['Date'].iloc[0].strftime(helper._date_str_fmt) != '01-Jun-2025'
        assert extract_df['Date'].iloc[-1].strftime(helper._date_str_fmt) == '01-Aug-2025'
        assert os.path.exists(os.path.join(tmp_dir, f'{index}_extract.csv'))

        # Pass test for correction and recovery cycles
        cr_df = analyzer.index_correction_recovery_cycles(
            csv_file=os.path.join(tmp_dir, f'{index}.csv'),
            excel_file=os.path.join(tmp_dir, f'{index}_correction_recovery.xlsx')
        )
        assert isinstance(cr_df, pandas.DataFrame)
        assert cr_df.shape[1] == 18
        assert os.path.exists(os.path.join(tmp_dir, f'{index}_correction_recovery.xlsx'))

        # Pass test for downloading daily data of another index
        index1 = 'NIFTY 50'
        daily_df = nse_tri.download_daily_data(
            index=index1,
            start_date='01-Jan-2021',
            csv_file=os.path.join(tmp_dir, f'{index1}.csv')
        )
        assert isinstance(daily_df, pandas.DataFrame)
        assert len(daily_df) > 0
        assert os.path.exists(os.path.join(tmp_dir, f'{index1}.csv'))

        # Pass test for CAGR yearly return
        cagr_df = cagr.index_yearly_return(
            csv_file=os.path.join(tmp_dir, f'{index}.csv'),
            excel_file=os.path.join(tmp_dir, f'{index}_cagr_yearly.xlsx')
        )
        assert isinstance(cagr_df, pandas.DataFrame)
        assert len(cagr_df) > 5
        assert os.path.exists(os.path.join(tmp_dir, f'{index}_cagr_yearly.xlsx'))

        # Pass test for SIP yearly return
        sip_df = sip.index_yearly_return(
            csv_file=os.path.join(tmp_dir, f'{index}.csv'),
            excel_file=os.path.join(tmp_dir, f'{index}_sip_yearly.xlsx')
        )
        assert isinstance(sip_df, pandas.DataFrame)
        assert len(sip_df) > 5
        assert os.path.exists(os.path.join(tmp_dir, f'{index}_sip_yearly.xlsx'))

        # Index list
        index_list = [
            index,
            index1
        ]

        # Pass test for CAGR indices comparison
        compare_df = cagr.indices_comparison(
            indices=index_list,
            dir_path=tmp_dir,
            excel_file=os.path.join(tmp_dir, 'cagr_compare.xlsx')
        )
        assert isinstance(compare_df, pandas.DataFrame)
        assert len(compare_df) == 2
        assert os.path.exists(os.path.join(tmp_dir, 'cagr_compare.xlsx'))

        # SIP indices comparison
        compare_df = sip.indices_comparison(
            indices=index_list,
            dir_path=tmp_dir,
            excel_file=os.path.join(tmp_dir, 'sip_compare.xlsx')
        )
        assert isinstance(compare_df, pandas.DataFrame)
        assert len(compare_df) == 2
        assert os.path.exists(os.path.join(tmp_dir, 'sip_compare.xlsx'))

        # Pass test for SIP from a give date
        sip_value = sip.index_return_from_given_date(
            csv_file=os.path.join(tmp_dir, f'{index}.csv'),
            yr_mon=(2022, 6)
        )
        assert isinstance(sip_value, pandas.Series)
        assert len(sip_value) == 8
        # Error test
        with pytest.raises(Exception) as exc_info:
            sip.index_return_from_given_date(
                csv_file=os.path.join(tmp_dir, f'{index}.csv'),
                yr_mon=(2020, 6)
            )
        assert 'SIP start date 01-Jun-2020 is outside the CSV date range' in exc_info.value.args[0]
