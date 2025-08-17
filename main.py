import sys
from typing import Callable, Dict, Type, Tuple, List, Any

from logs_handler.cli import init_parser, parse_args, ReportType
from logs_handler.reports import Report, AvgResponseTime, UserAgent
from logs_handler.utils import load_json, print_table

def build_report(file_path: str, ReportClass: Type[Report], filter_func: Callable[[Dict[str, Any]], bool] = lambda x: True) -> Tuple[List[List[Any]], List[str]]:
    """Builds the table and headers for tabulate to print."""
    report = ReportClass()
    try:
        lines_iter = filter(filter_func, load_json(file_path, report.get_required_fields()))

        for line in lines_iter:
            report.process_line(line)
        
        table = report.generate_table()
        headers = report.get_headers()

        return (table, headers)
    
    except ValueError as e:
        raise ValueError(f"Failed to process {file_path}: {e}")

def main():
    parser = init_parser()
    
    try:
        args = parse_args(parser)

        match args.report_type:
            case ReportType.AVERAGE:
                for file in args.input_files:
                    try:
                        # For filtering: 
                        # filter_func = lambda line: line.get("request_method") == "GET"
                        table, headers = build_report(file, AvgResponseTime, args.date_filter)
                        print_table(table, headers, file)
                    except ValueError as e:
                        print(f"Error while handling <{file}> file: {e}", file=sys.stderr)
                        continue

            case ReportType.USERAGENT:
                for file in args.input_files:
                    try:
                        # For filtering: 
                        # filter_func = lambda line: line.get("@timestamp") == "2025-06-22T13:57:32+00:00"
                        table, headers = build_report(file, UserAgent)
                        print_table(table, headers, file)
                    except ValueError as e:
                        print(f"Error while handling <{file}> file: {e}", file=sys.stderr)
                        continue
        
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(130)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()