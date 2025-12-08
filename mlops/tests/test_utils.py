def test_utils_import():
    from mlops.training.utils import clean_data
    assert callable(clean_data)
