from typing import Any, Dict, List
from .base import Report

class UserAgent(Report):
    HEADERS = ["browser", "count"]
    REQUIRED_FIELDS = ["http_user_agent"]

    def __init__(self) -> None:
        self.report: Dict[str, int] = {}

    def process_line(self, line: Dict[str, Any]) -> None:
        user_agent = line["http_user_agent"]

        self.report[user_agent] = self.report.get(user_agent, 0) + 1

    def generate_table(self) -> List[List[Any]]:
        sorted_report = sorted(self.report.items(), key=lambda item: item[1], reverse=True)
        return [[user_agent, count] for user_agent, count in sorted_report]
    
    def get_headers(self) -> List[str]:
        return self.HEADERS
    
    def get_required_fields(self) -> List[str]:
        return self.REQUIRED_FIELDS