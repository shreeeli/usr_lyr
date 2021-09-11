import pytest
from src import chck_res


@pytest.mark.parametrize("n,expected",[("sandwich",0),("toast",0)])
def test_lngth (base_chck,n,expected):
    assert (base_chck.collect())==0