import pytest


@pytest.mark.parametrize("index,data_name,remark_info", [1, 2, 3])
def test_change_remarks(index, data_name, remark_info):  # 列表传参
    index = 1
    data_name = 2
    remark_info = 3
