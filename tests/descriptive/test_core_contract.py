from fitlater.core.contract import build_contract


def test_build_contract_normal():
    dataset_meta = {
        "n_rows": 100,
        "n_cols": 5,
        "memory": "10KB"
    }

    profile = {
        "col1": {"mean": 10}
    }

    column_types = {
        "col1": "numeric",
        "col2": "categorical"
    }

    result = build_contract(dataset_meta, profile, column_types)

    assert isinstance(result, dict)

    # Check top-level keys
    assert "meta" in result
    assert "profile" in result
    assert "column_types" in result

    # Check values are passed correctly
    assert result["meta"] == dataset_meta
    assert result["profile"] == profile
    assert result["column_types"] == column_types


def test_build_contract_empty():
    result = build_contract({}, {}, {}, empty=True)

    assert isinstance(result, dict)

    # Check structure
    assert "meta" in result
    assert "profile" in result
    assert "column_types" in result

    # Check empty meta
    assert result["meta"]["n_rows"] == 0
    assert result["meta"]["n_cols"] == 0
    assert result["meta"]["memory"] == ""

    # Profile and column_types should be empty dicts
    assert result["profile"] == {}
    assert result["column_types"] == {}


def test_build_contract_empty_ignores_inputs():
    dataset_meta = {"n_rows": 999}
    profile = {"fake": "data"}
    column_types = {"col": "wrong"}

    result = build_contract(dataset_meta, profile, column_types, empty=True)

    # Should NOT use provided values
    assert result["meta"]["n_rows"] == 0
    assert result["profile"] == {}
    assert result["column_types"] == {}


def test_build_contract_missing_keys_allowed():
    """
    Your function does NOT validate structure,
    so it should accept any dict and pass it through.
    """
    dataset_meta = {}
    profile = {}
    column_types = {}

    result = build_contract(dataset_meta, profile, column_types)

    assert result["meta"] == {}
    assert result["profile"] == {}
    assert result["column_types"] == {}

def test_build_contract_does_not_mutate_inputs():
    dataset_meta = {"n_rows": 10}
    profile = {"a": 1}
    column_types = {"col": "num"}

    result = build_contract(dataset_meta, profile, column_types)

    result["meta"]["n_rows"] = 999

    # If this fails → you have a mutation bug
    assert dataset_meta["n_rows"] == 10

def test_build_contract_meta_keys_exist_in_empty():
    result = build_contract({}, {}, {}, empty=True)

    assert set(result["meta"].keys()) == {"n_rows", "n_cols", "memory"}

def test_build_contract_meta_types():
    dataset_meta = {
        "n_rows": 100,
        "n_cols": 5,
        "memory": "10KB"
    }

    result = build_contract(dataset_meta, {}, {})

    assert isinstance(result["meta"]["n_rows"], int)
    assert isinstance(result["meta"]["n_cols"], int)
    assert isinstance(result["meta"]["memory"], str)