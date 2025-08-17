from abc import ABC, abstractmethod
from typing import Any, Dict, List


class Report(ABC):
    """
    An abstract base class that defines the contract for all report types.
    """
    @abstractmethod
    def process_line(self, line: Dict[str, Any]) -> None:
        """Processes a single log entry to update the report's state."""
        pass

    @abstractmethod
    def generate_table(self) -> List[List[Any]]:
        """Generates the final table data from the aggregated report."""
        pass

    @abstractmethod
    def get_headers(self) -> List[str]:
        """Returns the list of header strings for the report's table."""
        pass

    @abstractmethod
    def get_required_fields(self) -> List[str]:
        """Returns the list of the fields log file should have."""