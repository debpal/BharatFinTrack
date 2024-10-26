import pytest
import BharatFinTrack
import os
import tempfile
import datetime
import pandas
import matplotlib.pyplot


@pytest.fixture(scope='class')
def nse_product():

    yield BharatFinTrack.NSEProduct()


@pytest.fixture(scope='class')
def nse_index():

    yield BharatFinTrack.NSEIndex()


@pytest.fixture(scope='class')
def nse_tri():

    yield BharatFinTrack.NSETRI()


@pytest.fixture(scope='class')
def visual():

    yield BharatFinTrack.Visual()


@pytest.fixture(scope='class')
def core():

    yield BharatFinTrack.core.Core()


@pytest.fixture
def message():

    output = {
        'error_category': 'Input category "region" does not exist.',
        'error_date1': "time data '16-Sep-202' does not match format '%d-%b-%Y'",
        'error_date2': "time data '20-Se-2024' does not match format '%d-%b-%Y'",
        'error_date3': 'Start date 27-Sep-2024 cannot be later than end date 26-Sep-2024.',
        'error_excel': 'Input file extension ".xl" does not match the required ".xlsx".',
        'error_figure': 'Input figure file extension is not supported.',
        'error_folder': 'The folder path does not exist.',
        'error_index1': '"INVALID" index does not exist.',
        'error_index2': '"NIFTY50 USD" index data is not available as open-source.',
        'error_df': 'Threshold values return an empty DataFrame.',
        'error_close': 'Invalid indices close value type: TRII; must be one of [PRICE, TRI].'

    }

    return output


def test_save_dataframes_equity_indices(
    nse_product,
    message
):

    with tempfile.TemporaryDirectory() as tmp_dir:
        excel_file = os.path.join(tmp_dir, 'equity.xlsx')
        df = nse_product.save_dataframe_equity_index_parameters(
            excel_file=excel_file
        )
        assert len(df.index.names) == 2


def test_get_equity_indices_by_category(
    nse_product,
    message
):

    # pass test
    assert 'NIFTY 500' in nse_product.get_equity_indices_by_category('broad')
    assert 'NIFTY IT' in nse_product.get_equity_indices_by_category('sector')
    assert 'NIFTY HOUSING' in nse_product.get_equity_indices_by_category('thematic')
    assert 'NIFTY ALPHA 50' in nse_product.get_equity_indices_by_category('strategy')
    assert 'NIFTY50 USD' in nse_product.get_equity_indices_by_category('variant')

    # error test
    with pytest.raises(Exception) as exc_info:
        nse_product.get_equity_indices_by_category('region')
    assert exc_info.value.args[0] == message['error_category']


def test_is_index_exist(
    nse_product
):

    assert nse_product.is_index_exist('NIFTY 100') is True
    assert nse_product.is_index_exist('INVALID') is False


def test_get_equity_index_base_date(
    nse_product,
    message
):

    # pass test
    assert nse_product.get_equity_index_base_date('NIFTY100 EQUAL WEIGHT') == '01-Jan-2003'
    assert nse_product.get_equity_index_base_date('NIFTY INDIA DEFENCE') == '02-Apr-2018'

    # error test
    with pytest.raises(Exception) as exc_info:
        nse_product.get_equity_index_base_date('INVALID')
    assert exc_info.value.args[0] == message['error_index1']


def test_get_equity_index_base_value(
    nse_product,
    message
):

    # pass test
    assert nse_product.get_equity_index_base_value('NIFTY MIDCAP LIQUID 15') == 1500.0
    assert nse_product.get_equity_index_base_value('NIFTY IT') == 100.0

    # error test
    with pytest.raises(Exception) as exc_info:
        nse_product.get_equity_index_base_value('INVALID')
    assert exc_info.value.args[0] == message['error_index1']


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


def test_download_historical_daily_data(
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
        # pass test for start date being None
        df = nse_tri.download_historical_daily_data(
            index='NIFTY INDIA DEFENCE',
            excel_file=excel_file,
            start_date=None,
            end_date='10-Apr-2018'
        )
        assert float(df.iloc[0, -1]) == 1000.00
        # pass test for end date being None
        start_date = (datetime.date.today() - datetime.timedelta(days=7)).strftime('%d-%b-%Y')
        df = nse_tri.download_historical_daily_data(
            index='NIFTY 50',
            excel_file=excel_file,
            start_date=start_date,
            end_date=None
        )
        assert len(df) > 0


@pytest.mark.parametrize(
    'index, expected_value',
    [
        ('NIFTY TOP 20 EQUAL WEIGHT', 12041.27),
        ('NIFTY INDIA NEW AGE CONSUMPTION', 14709.71),
    ]
)
def test_index_download_historical_daily_data(
    nse_tri,
    index,
    expected_value
):
    with tempfile.TemporaryDirectory() as tmp_dir:
        excel_file = os.path.join(tmp_dir, 'output.xlsx')
        df = nse_tri.download_historical_daily_data(
            index=index,
            excel_file=excel_file,
            start_date='15-Oct-2024',
            end_date='15-Oct-2024'
        )
        assert float(df.iloc[-1, -1]) == expected_value


def test_equity_index_price_download_updated_value(
    nse_index,
    message,
    capsys
):

    # error test for folder path
    with tempfile.TemporaryDirectory() as tmp_dir:
        pass
    with pytest.raises(Exception) as exc_info:
        nse_index.download_daily_summary_report(tmp_dir)
    assert exc_info.value.args[0] == message['error_folder']
    # pass test for capturing print statement
    nse_index.equity_cagr_from_launch(
        untracked_indices=True
    )
    capture_print = capsys.readouterr()
    assert 'List of untracked download indices' in capture_print.out
    assert 'List of untracked base indices' in capture_print.out

    # pass test for sorting of NSE equity indices by CAGR (%) value
    with tempfile.TemporaryDirectory() as tmp_dir:
        excel_file = os.path.join(tmp_dir, 'equity.xlsx')
        nse_index.sort_equity_cagr_from_launch(
            excel_file=excel_file
        )
        df = pandas.read_excel(excel_file)
        assert len(df.index.names) == 1

    # pass test for categorical sorting NSE equity indices by CAGR (%) value
    with tempfile.TemporaryDirectory() as tmp_dir:
        excel_file = os.path.join(tmp_dir, 'equity.xlsx')
        nse_index.category_sort_equity_cagr_from_launch(
            excel_file=excel_file
        )
        df = pandas.read_excel(excel_file, index_col=[0, 1])
        assert df.shape[1] == 9
        assert len(df.index.get_level_values('Category').unique()) <= 5


def test_equity_index_tri_closing(
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
        df = nse_tri.compare_cagr_over_price(
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
                figure_file=os.path.join(tmp_dir, 'error_figure_file.pn'),
                close_type='TRI'
            )
        assert exc_info.value.args[0] == message['error_figure']
        # error test for invalid figure file input
        with pytest.raises(Exception) as exc_info:
            visual.plot_cagr_filtered_indices_by_category(
                excel_file=output_excel,
                figure_file=os.path.join(tmp_dir, 'error_figure_file.pn'),
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
        # error test for invalid figure file input
        with pytest.raises(Exception) as exc_info:
            visual.plot_cagr_filtered_indices(
                excel_file=output_excel,
                figure_file=os.path.join(tmp_dir, 'error_figure_file.pn'),
                close_type='TRI'
            )
        assert exc_info.value.args[0] == message['error_figure']
        # error test for invalid figure file input
        with pytest.raises(Exception) as exc_info:
            visual.plot_cagr_filtered_indices(
                excel_file=output_excel,
                figure_file=os.path.join(tmp_dir, 'error_figure_file.pn'),
                close_type='TRII'
            )
        assert exc_info.value.args[0] == message['error_close']


def test_update_historical_daily_data(
    nse_tri
):

    with tempfile.TemporaryDirectory() as tmp_dir:
        excel_file = os.path.join(tmp_dir, 'equity.xlsx')
        today = datetime.date.today()
        day1_ago = today - datetime.timedelta(days=30)
        day2_ago = today - datetime.timedelta(days=15)
        # pass test for downloading daily TRI values of NSE a equity index
        nse_tri.download_historical_daily_data(
            index='NIFTY 50',
            excel_file=excel_file,
            start_date=day1_ago.strftime('%d-%b-%Y'),
            end_date=day2_ago.strftime('%d-%b-%Y')
        )
        len_df1 = len(pandas.read_excel(excel_file))
        # pass test for updating daily TRI values for the NSE equity index
        nse_tri.update_historical_daily_data(
            index='NIFTY 50',
            excel_file=excel_file
        )
        len_df2 = len(pandas.read_excel(excel_file))
        assert len_df2 > len_df1


def test_error_excel(
    nse_product,
    nse_index,
    nse_tri,
    message
):

    with pytest.raises(Exception) as exc_info:
        nse_product.save_dataframe_equity_index_parameters(
            excel_file=r"C:\Users\Username\Folder\out.xl"
        )
    assert exc_info.value.args[0] == message['error_excel']

    with pytest.raises(Exception) as exc_info:
        nse_index.sort_equity_cagr_from_launch(
            excel_file='equily.xl'
        )
    assert exc_info.value.args[0] == message['error_excel']

    with pytest.raises(Exception) as exc_info:
        nse_index.category_sort_equity_cagr_from_launch(
            excel_file='equily.xl'
        )
    assert exc_info.value.args[0] == message['error_excel']

    with pytest.raises(Exception) as exc_info:
        nse_tri.download_historical_daily_data(
            index='NIFTY 50',
            start_date='23-Sep-2024',
            end_date='27-Sep-2024',
            excel_file='NIFTY50_tri.xl'
        )
    assert exc_info.value.args[0] == message['error_excel']

    with pytest.raises(Exception) as exc_info:
        nse_tri.download_daily_summary_equity_closing(
            excel_file='output.xl'
        )
    assert exc_info.value.args[0] == message['error_excel']

    with pytest.raises(Exception) as exc_info:
        nse_tri.sort_equity_value_from_launch(
            input_excel='input.xlsx',
            output_excel='output.xl'
        )
    assert exc_info.value.args[0] == message['error_excel']

    with pytest.raises(Exception) as exc_info:
        nse_tri.category_sort_equity_cagr_from_launch(
            input_excel='input.xlsx',
            output_excel='output.xl'
        )
    assert exc_info.value.args[0] == message['error_excel']

    with pytest.raises(Exception) as exc_info:
        nse_tri.sort_equity_cagr_from_launch(
            input_excel='input.xlsx',
            output_excel='output.xl'
        )
    assert exc_info.value.args[0] == message['error_excel']

    with pytest.raises(Exception) as exc_info:
        nse_tri.category_sort_equity_cagr_from_launch(
            input_excel='input.xlsx',
            output_excel='output.xl'
        )
    assert exc_info.value.args[0] == message['error_excel']

    with pytest.raises(Exception) as exc_info:
        nse_tri.compare_cagr_over_price(
            tri_excel='input.xlsx',
            price_excel='input.xlsx',
            output_excel='output.xl'
        )
    assert exc_info.value.args[0] == message['error_excel']
