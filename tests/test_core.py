import pytest
import BharatFinTrack


@pytest.fixture(scope='class')
def core():

    yield BharatFinTrack.core.Core()


def test_error_sip_growth(
    core
):

    with pytest.raises(Exception) as exc_info:
        core.sip_growth(
            invest=1000,
            frequency='monthlyy',
            annual_return=7.5,
            years=20
        )
    assert exc_info.value.args[0] == "Select a valid frequency from ['yearly', 'quarterly', 'monthly', 'weekly']"


def test_github_action(
    core
):

    assert core._github_action(
        integer=4
    ) == '4'
