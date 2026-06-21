# File Organizer

A simple Python script that automatically organizes files in the current project folder by their **last modified date**.

## What it does

The script:
- scans the source directory for files,
- creates folders by year and by month (for example, `2026/Jun-2026`),
- moves files into those folders,
- generates a report in both text and CSV formats.

## Features

- **Date-based sorting** using file modification time
- **Automatic folder creation** for each year and month
- **Duplicate-safe moving** (avoids overwriting files with same name)
- **Report generation** for summary results

## Project structure

```text
File system project/
├── file_organizer.py
├── Organised/
│   ├── file_report.txt
│   └── file_report.csv
└── README.md
```

## How to run

1. Make sure Python is installed.
2. Open the project folder in a terminal.
3. Run:

```bash
python file_organizer.py
```

## Output format

Files are moved into this structure:

```text
Organised/
└── 2026/
    └── Jun-2026/
        └── example.pdf
```

The script also creates:
- `Organised/file_report.txt` — readable summary
- `Organised/file_report.csv` — spreadsheet-friendly summary

## Notes

The script skips these files so they are not moved:
- `file_organizer.py`
- `file_report.txt`
- `file_report.csv`

## Author

Sourodip Das Gupta
