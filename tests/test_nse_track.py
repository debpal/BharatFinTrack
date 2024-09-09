import pytest
import BharatFinTrack

@pytest.fixture(scope='module')
def class_instance():
    
    return BharatFinTrack.NSETrack()
    
    
def test_get_indices_by_category(class_instance):
    
    # pass test
    assert class_instance.get_indices_by_category('broad')[0] == 'NIFTY 500'
    assert 'NIFTY ALPHA 50' in class_instance.get_indices_by_category('strategy')
    
    # error test
    with pytest.raises(Exception) as exc_info:
        class_instance.get_indices_by_category('non-existence')
    assert exc_info.value.args[0] == 'Invadid category: non-existence'
    
    
def test_is_downloadable_index(class_instance):

    assert class_instance.is_downloadable_index('NIFTY 50') == True
    assert class_instance.is_downloadable_index('non-existence') == False
    
    
def test_get_index_base_date(class_instance):

    assert class_instance.get_index_base_date('NIFTY 50') == '03-Nov-1995'
    
    # error test
    with pytest.raises(Exception) as exc_info:
        class_instance.get_index_base_date('non-existence')
    assert exc_info.value.args[0] == 'Invalid index: non-existence'
    
    
def test_get_index_base_value(class_instance):

    assert class_instance.get_index_base_value('NIFTY 50') == 1000.0
    assert class_instance.get_index_base_value('NIFTY IT') == 100.0
    
    # error test
    with pytest.raises(Exception) as exc_info:
        class_instance.get_index_base_value('non-existence')
    assert exc_info.value.args[0] == 'Invalid index: non-existence'
    