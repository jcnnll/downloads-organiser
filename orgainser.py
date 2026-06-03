import argparse
from pathlib import Path
import logging
import shutil
import re
import time


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("file_sorter.log"), logging.StreamHandler()],
)

DEFAULT_PATH = Path.home() / "Downloads"

FILE_TYPES = {
    "Images": ["jpg", "jpeg", "png", "gif", "webp"],
    "Documents": ["doc", "docx", "txt"],
    "PDFs": ["pdf"],
    "Spreadsheets": ["xls", "xlsx", "csv"],
    "Archive": ["zip"],
    "Videos": ["mp4", "mov"],
    "Software": ["dmg"],
    "Config": ["json", "yml", "yaml"],
}

IGNORED_FILES = {
    ".DS_Store",
    ".localized",
    "Thumbs.db",
}

IGNORED_EXTENSIONS = {
    ".crdownload",   # Chrome partial download
    ".part",         # Firefox partial download
    ".download",     # Safari/other browsers
}

EXTENSION_MAP = {
    ext.lower().strip("."): category
    for category, extensions in FILE_TYPES.items()
    for ext in extensions
}


def is_file_stable(file_path: Path, wait: float = 0.3) -> bool:
    """Checks if file size is stable (not actively downloading/writing)."""
    try:
        size_1 = file_path.stat().st_size
        time.sleep(wait)
        size_2 = file_path.stat().st_size
        return size_1 == size_2
    except FileNotFoundError:
        return False
    

def get_unique_destination(destination_file: Path) -> Path:
    """Ensures that the destination file does not get overwritten."""

    parent = destination_file.parent
    stem = destination_file.stem
    suffix = destination_file.suffix

    match = re.match(r"^(.*)_(\d+)$", stem)

    if match:
        base_name = match.group(1)
        counter = int(match.group(2)) + 1
    else:
        base_name = stem
        counter = 1

    next_path = destination_file

    while next_path.exists():
        next_path = parent / f"{base_name}_{counter}{suffix}"
        counter += 1

    return next_path


def move_file(
    source: Path, destination_dir: Path, is_uncategorised: bool = False, dry_run: bool = False
) -> None:
    """Handles directory creation, file movement, and scoped logging."""
    try:
        destination_dir.mkdir(parents=True, exist_ok=True)
        destination_file = get_unique_destination(destination_dir / source.name)

        if dry_run:
            logging.info(f"[DRY RUN] Would move '{source.name}' -> '{destination_dir.name}/{destination_file.name}'")
            return

        shutil.move(str(source), str(destination_file))

        if is_uncategorised:
            logging.warning(
                f"Moved uncategorised file '{source.name}' -> '{destination_dir.name}/{destination_file.name}'"
            )
        else:
            logging.info(f"Moved '{source.name}' -> '{destination_dir.name}/{destination_file.name}'")

    except Exception as e:
        logging.error(f"Failed to move '{source.name}': {e}")


def sort_target_folder(target_path: Path, dry_run: bool = False) -> None:
    """Iterates over the target folder and sorts files by extension."""
    logging.info(f"Starting to sort for: '{target_path}'")

    if not target_path.exists():
        logging.error(f"Target directory does not exist: {target_path}")
        return

    try:
        for file_path in target_path.iterdir():
            if not file_path.is_file():
                continue

            if time.time() - file_path.stat().st_mtime < 5:
                if not is_file_stable(file_path):
                    continue

            if file_path.name in IGNORED_FILES:
                continue

            if file_path.suffix.lower() in IGNORED_EXTENSIONS:
                continue
            

            file_ext = file_path.suffix.lower().strip(".")
            category = EXTENSION_MAP.get(file_ext)

            if category:
                move_file(file_path, target_path / category, dry_run=dry_run)
            else:
                move_file(file_path, target_path / "Other", is_uncategorised=True, dry_run=dry_run)

        logging.info(f"Completed sorting for: '{target_path}'")

    except Exception as e:
        logging.critical(f"Script crashed due to unexpected error: {e}")


if __name__ == "__main__":
    # Set up the command-line argument parser
    parser = argparse.ArgumentParser(
        description="A script to automatically sort files in a directory by extension."
    )
    parser.add_argument(
        "target_dir",
        type=str,
        nargs="?",
        default=str(DEFAULT_PATH),
        help="Path to the directory you want to sort (defaults to user Downloads folder)",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be moved without actully moving files",
    )

    args = parser.parse_args()

    # Convert the string input into a Path object
    target_path = Path(args.target_dir)

    sort_target_folder(target_path, args.dry_run)
