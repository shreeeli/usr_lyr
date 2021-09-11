from src import chck_res
import pytest

@pytest.fixture(scope="module")
def base_chck():
    data="sandwich"
    return (chck_res(data))
    