import pytest
import BharatFinTrack
import pandas


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


@pytest.fixture
def message():

    output = {
        'error_excel': 'Input file extension ".xl" does not match the required ".xlsx".',
        'error_figure': 'Input figure file extension is not supported.'
    }

    return output


def test_error_file_excel(
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
            csv_file='input.csv',
            excel_file='equily.xl'
        )
    assert exc_info.value.args[0] == message['error_excel']

    with pytest.raises(Exception) as exc_info:
        nse_index.category_sort_equity_cagr_from_launch(
            csv_file='input.csv',
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
        nse_tri.extract_historical_daily_data(
            input_excel='input.xlsx',
            start_date='23-Sep-2024',
            end_date='27-Sep-2024',
            output_excel='output.xl'
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
        nse_tri.compare_cagr_over_price_from_launch(
            tri_excel='input.xlsx',
            price_excel='input.xlsx',
            output_excel='output.xl'
        )
    assert exc_info.value.args[0] == message['error_excel']

    with pytest.raises(Exception) as exc_info:
        nse_tri.yearwise_sip_analysis(
            input_excel='input.xlsx',
            monthly_invest=1000,
            output_excel='output.xl'
        )
    assert exc_info.value.args[0] == message['error_excel']

    with pytest.raises(Exception) as exc_info:
        nse_tri.yearwise_cagr_analysis(
            input_excel='input.xlsx',
            output_excel='output.xl'
        )
    assert exc_info.value.args[0] == message['error_excel']

    with pytest.raises(Exception) as exc_info:
        nse_tri.yearwise_sip_xirr_growth_comparison_across_indices(
            indices=['NIFTY 50'],
            folder_path=r"C:\Users\Username\Folder",
            excel_file='output.xl'
        )
    assert exc_info.value.args[0] == message['error_excel']

    with pytest.raises(Exception) as exc_info:
        nse_tri.yearwise_cagr_growth_comparison_across_indices(
            indices=['NIFTY 50'],
            folder_path=r"C:\Users\Username\Folder",
            excel_file='output.xl'
        )
    assert exc_info.value.args[0] == message['error_excel']

    with pytest.raises(Exception) as exc_info:
        nse_tri.analyze_correction_recovery(
            input_excel='input.xlsx',
            output_excel='output.xl'
        )
    assert exc_info.value.args[0] == message['error_excel']


def test_error_file_figure(
    visual,
    message
):

    with pytest.raises(Exception) as exc_info:
        visual._mi_df_bar_closing_with_category(
            df=pandas.DataFrame(),
            close_type='TRI',
            index_type='NSE Equity',
            figure_title='title',
            figure_file='figure_file.pn'
        )
    assert exc_info.value.args[0] == message['error_figure']

    with pytest.raises(Exception) as exc_info:
        visual._df_bar_closing(
            df=pandas.DataFrame(),
            close_type='TRI',
            index_type='NSE Equity',
            figure_title='title',
            figure_file='figure_file.pn'
        )
    assert exc_info.value.args[0] == message['error_figure']

    with pytest.raises(Exception) as exc_info:
        visual.plot_yearwise_sip_returns(
            index='NIFTY 50',
            excel_file='NIFTY 50.xlsx',
            figure_file='figure_file.pn',
            ytick_gap=250
        )
    assert exc_info.value.args[0] == message['error_figure']

    with pytest.raises(Exception) as exc_info:
        visual.plot_sip_index_vs_gsec(
            index='NIFTY 50',
            excel_file='NIFTY 50.xlsx',
            figure_file='figure_file.pn',
            gsec_return=7.5,
            ytick_gap=500
        )
    assert exc_info.value.args[0] == message['error_figure']

    with pytest.raises(Exception) as exc_info:
        visual.plot_sip_growth_comparison_across_indices(
            indices=['NIFTY 50', 'NIFTY 500'],
            folder_path=r"C:\Users\Username\Folder",
            figure_file='figure_file.pn',
            ytick_gap=2
        )
    assert exc_info.value.args[0] == message['error_figure']
