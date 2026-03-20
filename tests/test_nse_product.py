import pytest
import BharatFinTrack
import tempfile
import os


@pytest.fixture(scope='class')
def nse_product():

    yield BharatFinTrack.NSEProduct()


@pytest.fixture(scope='class')
def helper():

    yield BharatFinTrack.helper.Helper()


def test_equity_base_parameter_midf(
    nse_product
):

    # Pass test
    with tempfile.TemporaryDirectory() as tmp_dir:
        excel_file = os.path.join(tmp_dir, 'equity.xlsx')
        df = nse_product.equity_base_parameter_midf(
            excel_file=excel_file
        )
        assert len(df.index.names) == 2


def test_equity_categorical_indices(
    nse_product
):

    # Pass test
    assert 'NIFTY 500' in nse_product.equity_categorical_indices('broad')
    assert 'NIFTY IT' in nse_product.equity_categorical_indices('sector')
    assert 'NIFTY HOUSING' in nse_product.equity_categorical_indices('thematic')
    assert 'NIFTY ALPHA 50' in nse_product.equity_categorical_indices('strategy')


def test_equity_index_base_parameters(
    nse_product,
    helper
):

    # Pass test
    index_df = nse_product.equity_index_base_parameters(
        index='NIFTY100 EQUAL WEIGHT'
    )
    assert index_df['Index Name'].iloc[0] == 'NIFTY100 EQUAL WEIGHT'
    assert index_df['Base Date'].iloc[0].strftime(helper._date_str_fmt) == '01-Jan-2003'
    assert index_df['Base Value'].iloc[0] == 1000
