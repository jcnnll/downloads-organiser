from pathlib import Path
import shutil

downloads_path = Path.home() / "Downloads"

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

print(f'Sorting {downloads_path}...')

for file_path in downloads_path.iterdir():
    if file_path.is_file():
        file_ext = file_path.suffix.lower().strip('.')

        moved = False

        for category, extensions in FILE_TYPES.items():
            cleaned_extensions = [ext.lower().strip('.') for ext in extensions]
            
            if file_ext in cleaned_extensions:
                destination_path = downloads_path / category
                destination_path.mkdir(exist_ok=True)
                file_path.rename(destination_path / file_path.name)

                moved = True
                break

        if not moved:
            destination_path = downloads_path / "Other"
            destination_path.mkdir(exist_ok=True)
            file_path.rename(destination_path / file_path.name)
