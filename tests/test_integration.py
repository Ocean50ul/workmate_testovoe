from pathlib import Path
import pathlib
from typing import Any, Dict
import pytest

from main import build_report
from logs_handler.reports import AvgResponseTime, UserAgent

FIXTURES_DIR = Path(__file__).parent / "fixtures"

def test_build_report_valid_json_no_filter():
    valid_log_file = FIXTURES_DIR / "valid.log"
    table, headers = build_report(str(valid_log_file), AvgResponseTime)

    assert len(table) == 3
    assert headers == AvgResponseTime.HEADERS

def test_build_report_valid_json_with_filter():
    def some_filter(line: Dict[str, Any]) -> bool:
        return line["url"] == "/api/context/..."
    
    valid_log_file = FIXTURES_DIR / "valid.log"
    table, headers = build_report(str(valid_log_file), AvgResponseTime, some_filter)

    assert len(table) == 1
    assert headers == AvgResponseTime.HEADERS

def test_build_malformed_json_with_filter():
    def some_filter(line: Dict[str, Any]) -> bool:
        return line["url"] == "/api/context/..."
    
    valid_log_file = FIXTURES_DIR / "malformed.log"
    with pytest.raises(ValueError):
        build_report(str(valid_log_file), AvgResponseTime, some_filter)

def test_build_report_polymorphism():
    valid_log_file = FIXTURES_DIR / "valid.log"
    avg_table, avg_headers = build_report(str(valid_log_file), AvgResponseTime)
    agent_table, agent_headers = build_report(str(valid_log_file), UserAgent)

    assert len(avg_table) == 3
    assert avg_headers == AvgResponseTime.HEADERS
    assert len(agent_table) == 1
    assert agent_headers == UserAgent.HEADERS

def test_build_empty_file(tmp_path: pathlib.Path):
    empty_file = tmp_path / "emtpy_file.log"
    empty_file.write_text("")

    table, _headers = build_report(str(empty_file), AvgResponseTime)
    assert len(table) == 0