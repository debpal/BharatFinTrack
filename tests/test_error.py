import pytest
import BharatFinTrack
import tempfile
import os
# import pandas


@pytest.fixture(scope='class')
def nse_product():

    yield BharatFinTrack.NSEProduct()


@pytest.fixture(scope='class')
def sip():

    yield BharatFinTrack.SIP()


def test_nse_product(
    nse_product
):

    # Error test for invalid directory path
    with pytest.raises(Exception) as exc_info:
        nse_product.equity_base_parameter_midf(
            excel_file='invalid_dir/invalid_excel.xlsx'
        )
    assert exc_info.value.args[0] == 'Invalid directory path "invalid_dir" for the input file'

    # Error test for invalid Excel file extension
    with tempfile.TemporaryDirectory() as tmp_dir:
        with pytest.raises(Exception) as exc_info:
            nse_product.equity_base_parameter_midf(
                excel_file=os.path.join(tmp_dir, 'invalid_ext.json')
            )
        assert exc_info.value.args[0] == 'Input file extension ".json" does not match the required ".xlsx"'

    # Error test from invalid index category
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

    # Error test for invalid directory path
    with pytest.raises(Exception) as exc_info:
        sip.investment_growth(
            invest=1000,
            frequency='invalid_frquency',
            annual_return=15,
            years=15
        )
    assert 'Invalid frequency "invalid_frquency"' in exc_info.value.args[0]


def test_github():

    assert str(2) == '2'
