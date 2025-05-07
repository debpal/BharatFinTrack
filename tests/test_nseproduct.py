import pytest
import BharatFinTrack
import tempfile
import os


@pytest.fixture(scope='class')
def nse_product():

    yield BharatFinTrack.NSEProduct()


@pytest.fixture
def message():

    output = {
        'error_category': 'Input category "region" does not exist.',
        'error_index1': '"INVALID" index does not exist.'
    }

    return output


def test_save_dataframe_equity_index_parameters(
    nse_product,
    message
):

    # pass test
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

    # pass test
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
