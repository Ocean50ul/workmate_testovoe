from decimal import Decimal
import json
import sys
from typing import Any, Dict, Iterator, List

from tabulate import tabulate

def load_json(path: str, required_fields: List[str]) -> Iterator[Dict[str, Any]]:

    total_lines = 0
    valid_lines = 0
    malformed_json = 0
    missing_fields_counter = 0

    with open(path, "r") as file:
        
        for line_num, line in enumerate(file, 1):

            if not line.strip():
                continue

            total_lines += 1

            try:
                data: Dict[str, Any] = json.loads(line, parse_float=Decimal)
                missing = [f for f in required_fields if f not in data.keys()]

                if missing:
                    missing_fields_counter += 1
                    print(f"line {line_num} missing {missing} feilds", file=sys.stderr)

                    if total_lines >= 15 and missing_fields_counter == 15:
                        raise ValueError(
                            f"File {path} appears to have wrong structure\nExpected fields {required_fields} not found in the first {total_lines} lines."
                        )
                    
                    continue
                
                valid_lines += 1
                yield data

            except json.JSONDecodeError:
                malformed_json += 1
                print(f"malformed json line: {line}", file=sys.stderr)
        
        if total_lines > 0 and valid_lines == 0:
            raise ValueError(
                f"No valid log entries was found in {file}\nFile might be in wrong format or corrupted.\n({malformed_json} JSON parser errors, {missing_fields_counter} missing required fields.)"
            )
        

def print_table(table: List[Any], headers: List[str], file: str) -> None:
    header = f"            --- Report for: {file} ---"
    print("\n" + header)
    print(tabulate(table, headers, showindex="always"))