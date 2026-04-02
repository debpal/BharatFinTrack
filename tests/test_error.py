import pytest
import BharatFinTrack
import tempfile
import os


@pytest.fixture(scope='class')
def helper():

    yield BharatFinTrack.helper.Helper()


@pytest.fixture(scope='class')
def nse_product():

    yield BharatFinTrack.NSEProduct()


@pytest.fixture(scope='class')
def sip():

    yield BharatFinTrack.SIP()


@pytest.fixture(scope='class')
def visual():

    yield BharatFinTrack.Visual()


def test_helper(
    helper,
    nse_product
):

    # Error test for invalid static type input variable
    with pytest.raises(Exception) as exc_info:
        nse_product.equity_categorical_indices(
            category=1
        )
    assert exc_info.value.args[0] == 'Expected "category" to be "str", but got type "int"'

    # Error test for invalid index name
    with pytest.raises(Exception) as exc_info:
        helper._equity_index_base_param(
            index='NIFTY 501',
            check_open_source=True
        )
    assert exc_info.value.args[0] == 'Non-existent index name: "NIFTY 501"'

    # Error test for non open-source index
    with pytest.raises(Exception) as exc_info:
        helper._equity_index_base_param(
            index='NIFTY50 USD',
            check_open_source=True
        )
    assert exc_info.value.args[0] == 'Historical daily data is not open-source for the index: "NIFTY50 USD"'

    # Error test for end date later than start date
    with pytest.raises(Exception) as exc_info:
        helper._date_end_later_start(
            start_date='01-Jan-2026',
            end_date='01-Jan-2025'
        )
    assert exc_info.value.args[0] == 'Start date "01-Jan-2026" cannot be later than end date "01-Jan-2025"'

    # Error test for different end date in CSV files
    with pytest.raises(Exception) as exc_info:
        helper._validate_same_end_date_in_dfs(
            indices=[
                'index_1',
                'index_2'
            ],
            dir_path=os.path.join(
                os.path.dirname(__file__), 'sample_data', 'daily_data'
            )
        )
    assert 'Mismatch of end date for the index' in exc_info.value.args[0]


def test_nse_product(
    nse_product
):

    # Error test for invalid directory path
    with pytest.raises(Exception) as exc_info:
        nse_product.equity_base_parameter_midf(
            excel_file='invalid_dir/invalid_excel.xlsx'
        )
    assert exc_info.value.args[0] == 'Invalid directory path "invalid_dir" for the input file'

    # Error test for invalid file extension
    with tempfile.TemporaryDirectory() as tmp_dir:

        # Excel file extension
        with pytest.raises(Exception) as exc_info:
            nse_product.equity_base_parameter_midf(
                excel_file=os.path.join(tmp_dir, 'excel_ext.json')
            )
        assert exc_info.value.args[0] == 'Input file extension ".json" does not match the required ".xlsx"'

    # Error test for invalid index category
    with pytest.raises(Exception) as exc_info:
        nse_product.equity_categorical_indices(
            category='invalid_category'
        )
    assert 'Invalid category "invalid_category"' in exc_info.value.args[0]

    # Error test for invalid index
    with pytest.raises(Exception) as exc_info:
        nse_product.equity_index_base_parameters(
            index='INVALID'
        )
    assert exc_info.value.args[0] == 'Non-existent index name: "INVALID"'


def test_sip(
    sip
):

    # Error test for invalid frequency
    with pytest.raises(Exception) as exc_info:
        sip.investment_growth(
            invest=1000,
            frequency='invalid_frquency',
            annual_return='15',
            years=15
        )
    expected_type = ['int', 'float']
    assert exc_info.value.args[0] == f'Expected "annual_return" to be one of {expected_type}, but got type "str"'

    # Error test for invalid frequency
    with pytest.raises(Exception) as exc_info:
        sip.investment_growth(
            invest=1000,
            frequency='invalid_frquency',
            annual_return=15,
            years=15
        )
    assert 'Invalid frequency "invalid_frquency"' in exc_info.value.args[0]


def test_visual(
    visual
):

    # Error test for invalid directory path
    with pytest.raises(Exception) as exc_info:
        visual._validate_figure_file(
            figure_file='invalid_dir/invalid_figure.png'
        )
    assert exc_info.value.args[0] == 'Invalid directory path "invalid_dir" for the figure file'

    # Error test for invalid file extension
    with tempfile.TemporaryDirectory() as tmp_dir:

        # Figure file extension
        with pytest.raises(Exception) as exc_info:
            visual._validate_figure_file(
                figure_file=os.path.join(tmp_dir, 'fig_ext.pn')
            )
        assert 'Input figure_file extension ".pn" is not supported' in exc_info.value.args[0]


def test_github():

    assert str(1) == '1'
