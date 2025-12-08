def test_imports():
    try:
        from mlops.training.train_lead_model import run_training
    except Exception as e:
        raise AssertionError(f"Import failed: {e}")

    assert True
