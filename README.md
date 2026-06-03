# Simple File Organiser

A lightweight Python script that automatically organises files into categorised directories based on their file extensions.

By default, the script sorts files in your Downloads folder, but you can specify any target directory from the command line.

## Features

* Organises files by extension into category folders
* Automatically creates destination folders when needed
* Moves uncategorised files into an `Other` folder
* Logs file movements and errors
* Supports custom target directories via command-line arguments
* Uses only Python standard library modules

## Categories

| Category     | Extensions                     |
| ------------ | ------------------------------ |
| Images       | jpg, jpeg, png, gif, webp      |
| Documents    | doc, docx, txt                 |
| PDFs         | pdf                            |
| Spreadsheets | xls, xlsx, csv                 |
| Archive      | zip                            |
| Videos       | mp4, mov                       |
| Software     | dmg                            |
| Config       | json, yml, yaml                |
| Other        | Any file type not listed above |

## Usage

Sort the default Downloads folder:

```bash
python organiser.py
```

Sort a specific directory:

```bash
python organiser.py /path/to/folder
```

Example:

```bash
python organiser.py ~/Desktop/TestFiles
```

## Logging

The script writes logs to:

```text
file_sorter.log
```

and also outputs log messages to the console.

## Requirements

* Python 3.8+
* No external dependencies

## Example

Before:

```text
Downloads/
├── report.pdf
├── image.png
├── data.csv
```

After:

```text
Downloads/
├── PDFs/
│   └── report.pdf
├── Images/
│   └── image.png
├── Spreadsheets/
│   └── data.csv
```
