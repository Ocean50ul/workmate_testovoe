import pytest
from pathlib import Path

from logs_handler.utils import load_json
from logs_handler.reports.average_response_time import AvgResponseTime

FIXTURES_DIR = Path(__file__).parent / "fixtures"

def test_all_lines_valid():
    valid_log_file = FIXTURES_DIR / "valid.log"
    required_fields = AvgResponseTime.REQUIRED_FIELDS

    json_iter = load_json(str(valid_log_file), required_fields)
    lines = list(json_iter)

    assert len(lines) == 20

    for line in lines:
        for req_field in required_fields:
            assert req_field in line.keys()

def test_malformed_json():
    malformed_log_file = FIXTURES_DIR / "malformed.log"
    required_fields = AvgResponseTime.REQUIRED_FIELDS

    json_iter = load_json(str(malformed_log_file), required_fields)
    with pytest.raises(ValueError):
        _lines = list(json_iter)

def test_some_lines_missing_fields(capsys: pytest.CaptureFixture[str]):
    some_fiends_missing_file = FIXTURES_DIR / "some_missing_fields.log"
    required_fields = AvgResponseTime.REQUIRED_FIELDS

    json_iter = load_json(str(some_fiends_missing_file), required_fields)
    lines = list(json_iter)

    assert len(lines) == 17

    captured_errors = capsys.readouterr()
    assert captured_errors.err.count("line") == 3

def test_all_lines_missing_fields():
    all_missing_fields_file = FIXTURES_DIR / "all_missing_fields.log"
    required_fields = AvgResponseTime.REQUIRED_FIELDS

    json_iter = load_json(str(all_missing_fields_file), required_fields)
    with pytest.raises(ValueError):
        _lines = list(json_iter)