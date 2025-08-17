import argparse
import pathlib
import pytest
from unittest import mock

from logs_handler.cli.parser import validate_path, validate_report_type, init_parser, parse_args, ReportType, ParsedArgs

def test_validate_path_invalid():
    path = "./path/doesnt/exist.txt"
    with pytest.raises(argparse.ArgumentTypeError):
        validate_path(path)

def test_validate_path_valid(tmp_path: pathlib.Path):
    test_file = tmp_path / "test_file.txt"
    test_file.write_text("test content")

    validated_path = validate_path(str(test_file))

    assert validated_path == str(test_file)

def test_validate_report_type_invalid():
    report_type = "gibbresh"
    with pytest.raises(argparse.ArgumentTypeError):
        validate_report_type(report_type)

def test_validate_report_type_valid():
    for report_type in ReportType.valid_values():
        validated_type = validate_report_type(report_type)
        assert report_type == validated_type

def test_parse_args_valid(tmp_path: pathlib.Path):
    test_file = tmp_path / "test_file.txt"
    test_file.write_text("test content")

    parser = init_parser()
    input_file_path = str(test_file)
    report_type = "average"
    args = ["main.py", "-f", input_file_path, "-r", report_type]

    with mock.patch("sys.argv", args):
        parsed_args = parse_args(parser)

    assert isinstance(parsed_args, ParsedArgs)
    assert len(parsed_args.input_files) == 1
    assert parsed_args.input_files[0] == input_file_path
    assert parsed_args.report_type == ReportType.AVERAGE

def test_pars_args_multiple_files(tmp_path: pathlib.Path):
    test_file1 = tmp_path / "test_file1.txt"
    test_file2 = tmp_path / "test_file2.txt"

    test_file1.write_text("test content1")
    test_file2.write_text("test content2")

    parser = init_parser()

    args = ["main.py", "-f", str(test_file1), str(test_file2), "-r", "user-agent"]
    
    with mock.patch("sys.argv", args):
        parsed_args = parse_args(parser)
    
    assert len(parsed_args.input_files) == 2
    assert parsed_args.input_files == [str(test_file1), str(test_file2)]
    assert parsed_args.report_type == ReportType.USERAGENT

def test_parse_args_empty(capsys: pytest.CaptureFixture[str]):
    parser = init_parser()
    args = ["main.py"]

    with mock.patch("sys.argv", args):
        with pytest.raises(SystemExit) as excinfo:
            parse_args(parser)
        
        assert excinfo.value.code == 2
        expected_error = "The following arguments are required: -f/--file, -r/--report"
        captured_error = capsys.readouterr()
        assert expected_error == captured_error.err.strip().capitalize()

def test_parse_args_invalid_file(capsys: pytest.CaptureFixture[str]):
    parser = init_parser()
    invalid_path = "./file/doesnt/exist"
    args = ["main.py", "-f", invalid_path, "-r", "average"]

    with mock.patch("sys.argv", args):
        with pytest.raises(SystemExit) as excinfo:
            parse_args(parser)
        
        assert excinfo.value.code == 2
        captured_error = capsys.readouterr().err
        assert invalid_path in captured_error

def test_parse_args_invalid_report_type(capsys: pytest.CaptureFixture[str], tmp_path: pathlib.Path):
    test_file = tmp_path / "test_file.txt"
    test_file.write_text("test content")

    parser = init_parser()
    invalid_report_type = "gibbrish"
    args = ["main.py", "-f", str(test_file), "-r", invalid_report_type]

    with mock.patch("sys.argv", args):
        with pytest.raises(SystemExit) as excinfo:
            parse_args(parser)
        
        assert excinfo.value.code == 2
        captured_error = capsys.readouterr().err
        assert invalid_report_type in captured_error