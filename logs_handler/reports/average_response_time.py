from dataclasses import dataclass
from decimal import Decimal
from typing import Any, Dict, List

from .base import Report

@dataclass
class AggregatedData:
    total_time: Decimal = Decimal(0.0)
    count: int = 0

    @property
    def average(self) -> Decimal:
        """Calculates the average time."""
        if self.count == 0:
            return Decimal("0.0")
        return self.total_time / self.count


class AvgResponseTime(Report):
    HEADERS = ["handler", "total", "avg_response_time"]
    REQUIRED_FIELDS = ["url", "response_time"]

    def __init__(self) -> None:
        self.report: Dict[str, AggregatedData] = {}

    def process_line(self, line: Dict[str, Any]) -> None:
        url = line["url"]
        response_time = line["response_time"]

        agg_data = self.report.setdefault(url, AggregatedData())
        agg_data.total_time += response_time
        agg_data.count += 1

    def generate_table(self) -> List[List[Any]]:
        sorted_report = sorted(self.report.items(), key=lambda item: item[1].count, reverse=True)
        return [[url, data.count, data.average] for url, data in sorted_report]
    
    def get_headers(self) -> List[str]:
        return self.HEADERS
    
    def get_required_fields(self) -> List[str]:
        return self.REQUIRED_FIELDS