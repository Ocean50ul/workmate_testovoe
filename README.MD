Requirements: pytest, tabulate.

Usage: `python main.py --file file1.log file2.log --report average --date `

To add new report type.

    - Add new report class into the reports package. 

    - Add new enum variant to the cli pareser.

    - Add new match case to the main.



Any filtering is done via `build_report` function.
