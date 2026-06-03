import argparse
from pathlib import Path
import logging
import shutil

# Configure logging
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

EXTENSION_MAP = {
    ext.lower().strip("."): category
    for category, extensions in FILE_TYPES.items()
    for ext in extensions
}


def get_unique_destination(destination_file: Path) -> Path:
    """Ensures that the destination file does not get overwritten."""
    counter = 1

    while destination_file.exists():
        destination_file = (
            destination_file.parent
            / f"{destination_file.stem}_{counter}{destination_file.suffix}"
        )
        counter += 1

    return destination_file


def move_file(
    source: Path, destination_dir: Path, is_uncategorised: bool = False
) -> None:
    """Handles directory creation, file movement, and scoped logging."""
    try:
        destination_dir.mkdir(parents=True, exist_ok=True)
        destination_file = get_unique_destination(destination_dir / source.name)

        shutil.move(str(source), str(destination_file))

        if is_uncategorised:
            logging.warning(
                f"Moved uncategorised file '{source.name}' -> '{destination_dir.name}/{destination_file.name}'"
            )
        else:
            logging.info(f"Moved '{source.name}' -> '{destination_dir.name}/{destination_file.name}'")

    except Exception as e:
        logging.error(f"Failed to move '{source.name}': {e}")


def sort_target_folder(target_path: Path) -> None:
    """Iterates over the target folder and sorts files by extension."""
    logging.info(f"Starting to sort for: '{target_path}'")

    if not target_path.exists():
        logging.error(f"Target directory does not exist: {target_path}")
        return

    try:
        for file_path in target_path.iterdir():
            if not file_path.is_file():
                continue

            if file_path.name in IGNORED_FILES:
                continue

            file_ext = file_path.suffix.lower().strip(".")
            category = EXTENSION_MAP.get(file_ext)

            if category:
                move_file(file_path, target_path / category)
            else:
                move_file(file_path, target_path / "Other", is_uncategorised=True)

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

    args = parser.parse_args()

    # Convert the string input into a Path object
    target_path = Path(args.target_dir)

    sort_target_folder(target_path)
