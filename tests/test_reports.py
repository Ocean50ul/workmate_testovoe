from decimal import Decimal
from typing import Any, Dict
import pytest

from logs_handler.reports import AvgResponseTime
from logs_handler.reports.average_response_time import AggregatedData

def test_avg_process_valid_line():
    avg = AvgResponseTime()
    assert not avg.report

    valid_line: Dict[str, Any] = {"@timestamp": "2025-06-22T13:57:32+00:00", "status": 200, "url": "/api/context/...", "request_method": "GET", "response_time": Decimal("0.024"), "http_user_agent": "..."}
    avg.process_line(valid_line)

    assert avg.report.get("/api/context/...") == AggregatedData(Decimal("0.024"), 1)

def test_avg_process_invalid_line():
    avg = AvgResponseTime()
    assert not avg.report

    invalid_line: Dict[str, Any] = {"@timestamp": "2025-06-22T13:57:32+00:00", "status": 200, "invalid url key": "/api/context/...", "request_method": "GET", "response_time": Decimal("0.024"), "http_user_agent": "..."}
    with pytest.raises(KeyError):
        avg.process_line(invalid_line)

def test_avg_generate_table():
    avg = AvgResponseTime()
    assert not avg.report

    empty_table = avg.generate_table()
    assert not empty_table

def test_aggr_data_average():
    aggr_data = AggregatedData(Decimal("25.0"), 0)
    avg = aggr_data.average

    assert avg == Decimal("0.0")