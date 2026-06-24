import pytest
import BharatFinTrack
import tempfile
import os
import json


@pytest.fixture(scope='class')
def nps():

    yield BharatFinTrack.NPS()


def test_fecth_data(
    nps
):

    with tempfile.TemporaryDirectory() as tmp_dir:

        # Pass test for downloading base parameters
        df = nps._download_base_parameters()
        assert len(df) == 262

        # Pass test for saving base DataFrame
        df = nps.base_df(
            excel_file=os.path.join(tmp_dir, 'base_df.xlsx')
        )
        assert len(df) == 262
        assert os.path.exists(os.path.join(tmp_dir, 'base_df.xlsx'))

        # Pass test for NPS schemes latest NAV
        df = nps.schemes_latest_nav(
            scheme_ids=[
                'SM008018',
                'SM008019',
                'SM008020'
            ],
            excel_file=os.path.join(tmp_dir, 'scheme_latest_nav.xlsx')
        )
        assert len(df) == 3
        assert os.path.exists(os.path.join(tmp_dir, 'scheme_latest_nav.xlsx'))
        assert 'float' in str(df['NAV'].dtype)

        # Pass test for NPS scheme historical NAV
        df = nps.scheme_historical_nav(
            pfm_name='HDFC',
            scheme_id='SM008018',
            csv_file=os.path.join(tmp_dir, 'scheme_hisotrical_nav.csv')
        )

        assert len(df) > 3000
        assert os.path.exists(os.path.join(tmp_dir, 'scheme_hisotrical_nav.csv'))


def test_pfm_schemes(
    nps
):

    # Pass test for NPS schemes
    scheme_str = nps.pfm_schemes(
        pfm_name='HDFC'
    )

    scheme_dict = json.loads(
        s=scheme_str
    )

    assert isinstance(scheme_str, str)
    assert isinstance(scheme_dict, dict)
    assert len(scheme_dict) == 24
