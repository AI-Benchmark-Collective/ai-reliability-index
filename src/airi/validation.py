from __future__ import annotations

import json
from importlib.resources import files
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator


class ValidationFailure(ValueError):
    pass


def load_yaml(path: Path) -> dict[str, Any]:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise ValidationFailure(f"could not read {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise ValidationFailure(f"{path}: top-level value must be an object")
    return data


def load_schema(name: str) -> dict[str, Any]:
    schema_path = files("airi").joinpath("schemas", name)
    return json.loads(schema_path.read_text(encoding="utf-8"))


def validate_data(data: dict[str, Any], schema_name: str, source: str) -> None:
    validator = Draft202012Validator(load_schema(schema_name))
    errors = sorted(validator.iter_errors(data), key=lambda error: list(error.absolute_path))
    if not errors:
        return
    formatted = []
    for error in errors:
        location = ".".join(str(part) for part in error.absolute_path) or "<root>"
        formatted.append(f"{source}:{location}: {error.message}")
    raise ValidationFailure("\n".join(formatted))


def load_and_validate_task(path: Path) -> dict[str, Any]:
    task = load_yaml(path)
    validate_data(task, "task.schema.json", str(path))
    return task


def validate_result(result: dict[str, Any], source: str = "result") -> None:
    validate_data(result, "result.schema.json", source)
