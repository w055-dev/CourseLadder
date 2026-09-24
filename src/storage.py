"""Чтение и запись данных в JSON-файлы."""

import json
import os
from typing import Any


class StorageError(Exception):
    """Кастомная ошибка при работе с файловым хранилищем."""


def load_json(path: str) -> list[dict[str, Any]]:
    """Загружает список словарей из JSON-файла.
    Если файл отсутствует — возвращает пустой список.
    Если файл повреждён — выбрасывает StorageError.
    """
    if not os.path.exists(path):
        return []

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as exc:
        raise StorageError(f"Файл {path} повреждён: {exc}") from exc
    except OSError as exc:
        raise StorageError(f"Не удалось открыть {path}: {exc}") from exc

    if not isinstance(data, list):
        raise StorageError(f"Ожидался список в {path}")

    return data


def save_json(path: str, items: list[dict[str, Any]]) -> None:
    """Сохраняет список словарей в JSON-файл."""
    directory = os.path.dirname(path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)

    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(items, f, ensure_ascii=False, indent=2)
    except OSError as exc:
        raise StorageError(f"Не удалось записать {path}: {exc}") from exc
