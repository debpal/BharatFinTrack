import BharatFinTrack
import pytest


@pytest.fixture(scope='module')
def class_instance():
    
    print('call the module')
    
    return BharatFinTrack.NSETrack()
    
    
def test_indices_category(class_instance):
    
    output = class_instance.indices_category
    
    assert output == ['broad', 'sectoral', 'thematic', 'strategy']