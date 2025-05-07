import pytest
import BharatFinTrack
import os
import tempfile
import datetime
import pandas
import matplotlib.pyplot


@pytest.fixture(scope='class')
def nse_tri():

    yield BharatFinTrack.NSETRI()


@pytest.fixture(scope='class')
def visual():

    yield BharatFinTrack.Visual()


@pytest.fixture
def message():

    output = {
        'error_date1': "time data '16-Sep-202' does not match format '%d-%b-%Y'",
        'error_date2': "time data '20-Se-2024' does not match format '%d-%b-%Y'",
        'error_date3': 'Start date 27-Sep-2024 cannot be later than end date 26-Sep-2024.',
        'error_lastdate': 'Last date must be equal across all indices in the Excel files.',
        'error_index1': '"INVALID" index does not exist.',
        'error_index2': '"NIFTY50 USD" index data is not available as open-source.',
        'error_df': 'Threshold values return an empty DataFrame.',
        'error_close': 'Invalid indices close value type: TRII; must be one of [PRICE, TRI].'

    }

    return output


def test_is_index_data_open_source(
    nse_tri,
    message
):

    # pass test
    assert nse_tri.is_index_open_source('NIFTY 50') is True
    assert nse_tri.is_index_open_source('NIFTY50 USD') is False

    # error test
    with pytest.raises(Exception) as exc_info:
        nse_tri.is_index_open_source('INVALID')
    assert exc_info.value.args[0] == message['error_index1']


def test_equity_tri_daily_closing(
    nse_tri,
    message,
    visual
):

    with tempfile.TemporaryDirectory() as tmp_dir:
        excel_file = os.path.join(tmp_dir, 'equity.xlsx')
        # pass test for downloading updated TRI values of NSE equity indices
        nse_tri.download_daily_summary_equity_closing(
            excel_file=excel_file,
            test_mode=True
        )
        df = pandas.read_excel(excel_file)
        assert df.shape[1] == 6
        assert df.shape[0] <= 8
        # pass test for sorting of NSE equity indices by TRI values
        output_excel = os.path.join(tmp_dir, 'tri_sort_closing_value.xlsx')
        nse_tri.sort_equity_value_from_launch(
            input_excel=excel_file,
            output_excel=output_excel
        )
        df = pandas.read_excel(output_excel)
        assert df.shape[1] == 5
        # pass test for sorting of NSE equity indices by CAGR (%) value
        output_excel = os.path.join(tmp_dir, 'tri_sort_cagr.xlsx')
        nse_tri.sort_equity_cagr_from_launch(
            input_excel=excel_file,
            output_excel=output_excel
        )
        df = pandas.read_excel(output_excel)
        assert df.shape[1] == 9
        # pass test for categorical sorting NSE equity indices by CAGR (%) value
        output_excel = os.path.join(tmp_dir, 'tri_sort_cagr_by_category.xlsx')
        nse_tri.category_sort_equity_cagr_from_launch(
            input_excel=excel_file,
            output_excel=output_excel
        )
        df = pandas.read_excel(output_excel, index_col=[0, 1])
        assert len(df.index.get_level_values('Category').unique()) <= 4
        # pass test for excess TRI CAGR(%) over PRICE CAGR(%)
        df = nse_tri.compare_cagr_over_price_from_launch(
            tri_excel=os.path.join(tmp_dir, 'tri_sort_cagr.xlsx'),
            price_excel=os.path.join(tmp_dir, 'tri_sort_cagr.xlsx'),
            output_excel=os.path.join(tmp_dir, 'compare_tri_cagr_over_price.xlsx')
        )
        assert df['Difference(%)'].unique()[0] == 0
        ###################################################################
        # PASS TEST FOR PLOTTING WITH CATEGORY
        ###################################################################
        # pass test for plotting of index closing value, grouped by category, filtered by a threshold CAGR (%) since their launch
        figure_file = os.path.join(tmp_dir, 'plot_tri_sort_cage_filtered_by_category.png')
        assert os.path.exists(figure_file) is False
        figure = visual.plot_cagr_filtered_indices_by_category(
            excel_file=output_excel,
            figure_file=figure_file,
            close_type='TRI'
        )
        assert isinstance(figure, matplotlib.pyplot.Figure) is True
        assert os.path.exists(figure_file) is True
        # pass test for plotting of index closing value, grouped by category, with the top CAGR (%) in each category since their launch.
        figure_file = os.path.join(tmp_dir, 'plot_tri_top_cagr_by_category.png')
        assert os.path.exists(figure_file) is False
        figure = visual.plot_top_cagr_indices_by_category(
            excel_file=output_excel,
            figure_file=figure_file,
            close_type='TRI'
        )
        assert isinstance(figure, matplotlib.pyplot.Figure) is True
        assert os.path.exists(figure_file) is True
        assert sum([file.endswith('.png') for file in os.listdir(tmp_dir)]) == 2
        ###################################################################
        # PASS TEST FOR PLOTTING WITHOUT CATEGORY
        ###################################################################
        # pass test for plotting of index closing value, filtered by a threshold CAGR (%) since their launch
        figure_file = os.path.join(tmp_dir, 'plot_tri_sort_filtered_cagr.png')
        assert os.path.exists(figure_file) is False
        figure = visual.plot_cagr_filtered_indices(
            excel_file=os.path.join(tmp_dir, 'tri_sort_cagr.xlsx'),
            figure_file=figure_file,
            close_type='TRI'
        )
        assert isinstance(figure, matplotlib.pyplot.Figure) is True
        assert os.path.exists(figure_file) is True
        assert sum([file.endswith('.png') for file in os.listdir(tmp_dir)]) == 3
        # pass test for plotting of index closing value with the top CAGR (%) in each category since their launch.
        figure_file = os.path.join(tmp_dir, 'plot_tri_top_cagr.png')
        assert os.path.exists(figure_file) is False
        figure = visual.plot_top_cagr_indices(
            excel_file=os.path.join(tmp_dir, 'tri_sort_cagr.xlsx'),
            figure_file=figure_file,
            close_type='TRI'
        )
        assert isinstance(figure, matplotlib.pyplot.Figure) is True
        assert os.path.exists(figure_file) is True
        assert sum([file.endswith('.png') for file in os.listdir(tmp_dir)]) == 4
        ###################################################################
        # ERROR TEST FOR PLOTTING WITH CATEGORY
        ###################################################################
        # error test for empty DataFrame from threshold values
        with pytest.raises(Exception) as exc_info:
            visual.plot_cagr_filtered_indices_by_category(
                excel_file=output_excel,
                figure_file=figure_file,
                close_type='TRI',
                threshold_cagr=100
            )
        assert exc_info.value.args[0] == message['error_df']
        # error test for invalid figure file input
        with pytest.raises(Exception) as exc_info:
            visual.plot_cagr_filtered_indices_by_category(
                excel_file=output_excel,
                figure_file=os.path.join(tmp_dir, 'error_figure_file.png'),
                close_type='TRII'
            )
        assert exc_info.value.args[0] == message['error_close']
        ###################################################################
        # ERROR TEST FOR PLOTTING WITHOUT CATEGORY
        ###################################################################
        # error test for empty DataFrame from threshold values
        with pytest.raises(Exception) as exc_info:
            visual.plot_cagr_filtered_indices(
                excel_file=output_excel,
                figure_file=figure_file,
                close_type='TRI',
                threshold_cagr=100
            )
        assert exc_info.value.args[0] == message['error_df']
        # error test for invalid input of index close type
        with pytest.raises(Exception) as exc_info:
            visual.plot_cagr_filtered_indices(
                excel_file=output_excel,
                figure_file=os.path.join(tmp_dir, 'error_figure_file.png'),
                close_type='TRII'
            )
        assert exc_info.value.args[0] == message['error_close']


def test_donwload_cagr_sip(
    nse_tri,
    visual,
    message
):

    with tempfile.TemporaryDirectory() as tmp_dir:
        # pass test for downloading indices historical daily data
        index = 'NIFTY 50'
        index_df = nse_tri.download_historical_daily_data(
            index=index,
            excel_file=os.path.join(tmp_dir, f'{index}_download.xlsx'),
        )
        assert float(index_df.iloc[0, -1]) == 1256.38
        # pass test for extracting downloaded data
        input_excel = os.path.join(tmp_dir, f'{index}.xlsx')
        index_df = nse_tri.extract_historical_daily_data(
            input_excel=os.path.join(tmp_dir, f'{index}_download.xlsx'),
            start_date='15-Oct-2022',
            end_date='15-Oct-2024',
            output_excel=input_excel
        )
        assert float(index_df.iloc[0, -1]) == 25139.55
        # pass test for yearwise SIP analysis
        sip_df = nse_tri.yearwise_sip_analysis(
            input_excel=input_excel,
            monthly_invest=1000,
            output_excel=os.path.join(tmp_dir, 'yearwise_sip.xlsx')
        )
        assert float(round(sip_df.iloc[-1, -1], 1)) == 24.0
        assert float(round(sip_df.iloc[-1, -2], 1)) == 1.3
        # pass test for yearwise CAGR analysis
        cagr_df = nse_tri.yearwise_cagr_analysis(
            input_excel=input_excel,
            output_excel=os.path.join(tmp_dir, 'yearwise_cagr.xlsx')
        )
        assert float(round(cagr_df.iloc[0, -3], 1)) == 28.4
        assert float(round(cagr_df.iloc[-1, -3], 1)) == 21.6
        # pass test for SIP analysis from a fixed date
        sip_summary = nse_tri.sip_summary_from_given_date(
            excel_file=input_excel,
            start_year=2024,
            start_month=4,
            monthly_invest=1000
        )
        assert sip_summary['XIRR (%)'] == '18.4'
        # pass test for SIP analysis where given date is earlier that actual downloaded start date
        sip_summary = nse_tri.sip_summary_from_given_date(
            excel_file=input_excel,
            start_year=2021,
            start_month=4,
            monthly_invest=1000
        )
        assert sip_summary['Actual start date'] == '17-Oct-2022'
        # pass test for plotting yearwise SIP analysis
        figure_file = os.path.join(tmp_dir, f'sip_yearwise_{index}.png')
        visual.plot_yearwise_sip_returns(
            index=index,
            excel_file=input_excel,
            figure_file=figure_file,
            ytick_gap=25
        )
        assert os.path.exists(figure_file) is True
        # pass test for comparison plot of SIP for index and bank fixed depost
        figure_file = os.path.join(tmp_dir, f'sip_gsec_vs_{index}.png')
        visual.plot_sip_index_vs_gsec(
            index=index,
            excel_file=input_excel,
            figure_file=figure_file,
            gsec_return=7.5,
            ytick_gap=25
        )
        assert os.path.exists(figure_file) is True
        assert sum([file.endswith('.png') for file in os.listdir(tmp_dir)]) == 2
        # pass test for comparison plot of SIP for multiple indices
        figure_file = os.path.join(tmp_dir, 'sip_invest_growth_across_indices.png')
        visual.plot_sip_growth_comparison_across_indices(
            indices=[index],
            folder_path=tmp_dir,
            figure_file=figure_file
        )
        assert os.path.exists(figure_file) is True
        assert sum([file.endswith('.png') for file in os.listdir(tmp_dir)]) == 3
        # pass test for comparison of SIP for multiple indices
        index_1 = 'NIFTY MIDCAP150 MOMENTUM 50'
        nse_tri.download_historical_daily_data(
            index=index_1,
            excel_file=os.path.join(tmp_dir, f'{index_1}.xlsx'),
            start_date='15-Oct-2022',
            end_date='15-Oct-2024'
        )
        # pass test for yearwise monthly SIP XIRR(%) and growth comparison across indices
        sipaggregate_df = nse_tri.yearwise_sip_xirr_growth_comparison_across_indices(
            indices=[index, index_1],
            folder_path=tmp_dir,
            excel_file=os.path.join(tmp_dir, 'compare_yearwise_sip_xirr_across_indices.xlsx')
        )
        assert len(sipaggregate_df.columns) == 2
        # pass test for yearwise CAGR(%) and growth comparison across indices
        cagraggregate_df = nse_tri.yearwise_cagr_growth_comparison_across_indices(
            indices=[index, index_1],
            folder_path=tmp_dir,
            excel_file=os.path.join(tmp_dir, 'compare_yearwise_cagr_across_indices.xlsx')
        )
        assert len(cagraggregate_df.columns) == 2
        # pass test for updating daily TRI values for the NSE equity index
        update_df = nse_tri.update_historical_daily_data(
            index=index,
            excel_file=input_excel,
            all_data=False
        )
        assert float(update_df.iloc[0, -1]) == 37196.69
        # pass test for analyzing corrections and recoveries of index values
        cr_df = nse_tri.analyze_correction_recovery(
            input_excel=input_excel,
            output_excel=os.path.join(tmp_dir, 'correction_recovery.xlsx')
        )
        assert len(cr_df.columns) == 18
        # error test for unequal end date of two indices
        nse_tri.extract_historical_daily_data(
            input_excel=os.path.join(tmp_dir, f'{index_1}.xlsx'),
            start_date='15-Oct-2022',
            end_date='15-Sep-2024',
            output_excel=os.path.join(tmp_dir, f'{index_1}.xlsx')
        )
        with pytest.raises(Exception) as exc_info:
            visual.plot_sip_growth_comparison_across_indices(
                # indices=['NIFTY 50', 'NIFTY ALPHA 50'],
                indices=[index, index_1],
                folder_path=tmp_dir,
                figure_file=figure_file
            )
        assert exc_info.value.args[0] == message['error_lastdate']
        # error test of unequal last date for yearwise SIP XIRR(%) and growth comparison across indicess
        with pytest.raises(Exception) as exc_info:
            nse_tri.yearwise_sip_xirr_growth_comparison_across_indices(
                # indices=['NIFTY 50', 'NIFTY ALPHA 50'],
                indices=[index, index_1],
                folder_path=tmp_dir,
                excel_file=os.path.join(tmp_dir, 'compare_yearwise_sip_xirr_across_indices.xlsx')
            )
        assert exc_info.value.args[0] == message['error_lastdate']
        # error test of unequal last date for yearwise CAGR(%) and growth comparison across indicess
        with pytest.raises(Exception) as exc_info:
            nse_tri.yearwise_cagr_growth_comparison_across_indices(
                # indices=['NIFTY 50', 'NIFTY ALPHA 50'],
                indices=[index, index_1],
                folder_path=tmp_dir,
                excel_file=os.path.join(tmp_dir, 'compare_yearwise_cagr_across_indices.xlsx')
            )
        assert exc_info.value.args[0] == message['error_lastdate']
        # error test for invalid input of year and month
        with pytest.raises(Exception) as exc_info:
            nse_tri.sip_summary_from_given_date(
                excel_file=input_excel,
                start_year=int(datetime.date.today().year) + 3,
                start_month=1,
                monthly_invest=1000
            )
        assert exc_info.value.args[0] == 'Given year and month return an empty DataFrame.'


def test_error_download_index_date(
    nse_tri,
    message
):

    with tempfile.TemporaryDirectory() as tmp_dir:
        excel_file = os.path.join(tmp_dir, 'output.xlsx')
        # error test for non open-source index
        with pytest.raises(Exception) as exc_info:
            nse_tri.download_historical_daily_data(
                index='NIFTY50 USD',
                excel_file=excel_file,
                start_date='27-Sep-2024',
                end_date='27-Sep-2024'
            )
        assert exc_info.value.args[0] == message['error_index2']
        # error test for invalid start date input
        with pytest.raises(Exception) as exc_info:
            nse_tri.download_historical_daily_data(
                index='NIFTY 50',
                excel_file=excel_file,
                start_date='16-Sep-202',
                end_date='26-Sep-2024'
            )
        assert exc_info.value.args[0] == message['error_date1']
        # error test for invalid end date input
        with pytest.raises(Exception) as exc_info:
            nse_tri.download_historical_daily_data(
                index='NIFTY 50',
                excel_file=excel_file,
                start_date='16-Sep-2024',
                end_date='20-Se-2024'
            )
        assert exc_info.value.args[0] == message['error_date2']
        # error test for strat date later than end date
        with pytest.raises(Exception) as exc_info:
            nse_tri.download_historical_daily_data(
                index='NIFTY 50',
                excel_file=excel_file,
                start_date='27-Sep-2024',
                end_date='26-Sep-2024'
            )
        assert exc_info.value.args[0] == message['error_date3']
        # error test for strat date later than end date
        with pytest.raises(Exception) as exc_info:
            nse_tri.extract_historical_daily_data(
                input_excel=excel_file,
                start_date='27-Sep-2024',
                end_date='26-Sep-2024',
                output_excel=excel_file
            )
        assert exc_info.value.args[0] == message['error_date3']
