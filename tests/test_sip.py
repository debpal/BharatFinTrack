import pytest
import BharatFinTrack
import tempfile
import os


@pytest.fixture(scope='class')
def sip():

    yield BharatFinTrack.SIP()


def test_download(
    sip
):

    with tempfile.TemporaryDirectory() as tmp_dir:

        # Pass test for SIP investment growth
        df = sip.investment_growth(
            invest=1000,
            frequency='weekly',
            annual_return=15,
            years=15,
            excel_file=os.path.join(tmp_dir, 'sip_growth.xlsx')
        )
        assert len(df) == 15
        assert round(df.iloc[-1, -1], 2) == 3.41
        assert os.path.exists(os.path.join(tmp_dir, 'sip_growth.xlsx'))
