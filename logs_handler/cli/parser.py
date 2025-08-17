import argparse
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Protocol
from enum import Enum
import os
import sys

class ReportType(Enum):
    """Type that represents eliglble values for --report/-r cli argument"""
    AVERAGE = "average"
    USERAGENT = "user-agent"

    @classmethod
    def valid_values(cls) -> List[str]:
        return [e.value for e in cls]
    
class Validator(Protocol):
    def __call__(self, value: str) -> str: ...

@dataclass(frozen=True)
class Argument:
    """Class that represents a cli argument for argparser builder."""
    flags: List[str]
    type_validator: Validator
    dest: str
    nargs: str | None = None
    required: bool = True
    help: str = ""

@dataclass(frozen=True)
class ParsedArgs:
    """Class that represents parsed arguments."""
    input_files: List[str]
    report_type: ReportType
    date_filter: Callable[Dict[str, Any], bool]


def validate_path(value: str) -> str:
    """Function that validates whether a given path exist."""
    if not os.path.exists(value):
        raise argparse.ArgumentTypeError(f"file <{value}> not found.")
    return value

def validate_report_type(value: str) -> str:
    """Function that validates the report type string, inputted by user."""
    try:
        ReportType(value)
        return value
    except ValueError:
        valid_types = ReportType.valid_values()
        msg = f"invalid report type <{value}>. \nAvailable report types: {valid_types}"
        raise argparse.ArgumentTypeError(msg)

def mock_date_validator(value: str) -> str:
    return value

class CLIArguments(Enum):
    """Type that represents all implemented cli arguments."""

    FILE_PATHS = Argument(
        flags=["-f", "--file"],
        type_validator=validate_path,
        dest="input_files",
        nargs="+",
        required=True,
        help="Input file paths to process"
    )

    REPORT_TYPE = Argument(
        flags=["-r", "--report"],
        type_validator=validate_report_type,
        dest="report_type",
        nargs=None,
        required=True,
        help=f"Report type to generate. Options: {ReportType.valid_values()}"
    )

    DATE = Argument(
        flags=["-d", "--date"],
        type_validator=mock_date_validator,
        dest="date",
        nargs=None,
        required=False,
        help="Specify the date."
    )

    @classmethod
    def all_arguments(cls) -> List[Argument]:
        return [e.value for e in cls]


class CustomArgumentParser(argparse.ArgumentParser):
    """Stuff just for printing clear error messages. Jeeesh, argparser, you have some wierd quirks out there."""
    def error(self, message: str):
        sys.stderr.write(f'{message.capitalize()}\n')

        # Standard exit code for command-line usage errors
        sys.exit(2)


def init_parser() -> argparse.ArgumentParser:
    """Function that builds argparser."""
    parser = CustomArgumentParser()
    
    for arg_def in CLIArguments.all_arguments():
        parser.add_argument(
            *arg_def.flags,
            dest=arg_def.dest,
            help=arg_def.help,
            required=arg_def.required,
            nargs=arg_def.nargs,
            type=arg_def.type_validator
        )
    
    return parser

def parse_args(parser: argparse.ArgumentParser) -> ParsedArgs:
    args = parser.parse_args()
    date_filter = lambda x: True

    if args.date is not None:
        date_filter = lambda line: line["@timestamp"] == args.date

    return ParsedArgs(
        input_files=args.input_files,
        report_type=ReportType(args.report_type),
        date_filter=date_filter
    )

