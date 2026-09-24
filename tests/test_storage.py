"""Тесты чтения/записи JSON."""

import os
import pytest
from src.storage import load_json, save_json, StorageError


def test_save_and_load(tmp_path):
    path = str(tmp_path / "test.json")
    data = [{"id": 1, "name": "Test"}]
    save_json(path, data)
    assert load_json(path) == data


def test_load_missing_file_returns_empty(tmp_path):
    path = str(tmp_path / "missing.json")
    assert load_json(path) == []


def test_load_corrupted_file(tmp_path):
    path = str(tmp_path / "broken.json")
    with open(path, "w", encoding="utf-8") as f:
        f.write("{ not valid json")
    with pytest.raises(StorageError, match="повреждён"):
        load_json(path)


def test_save_creates_directory(tmp_path):
    path = str(tmp_path / "subdir" / "file.json")
    save_json(path, [{"a": 1}])
    assert os.path.exists(path)
