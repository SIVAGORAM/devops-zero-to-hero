from pathlib import Path
import shutil

def create_backup(source, destination):
    src, dst = Path(source), Path(destination)
    dst.mkdir(parents=True, exist_ok=True)
    if src.exists():
        backup_location = dst / src.name
        if src.is_dir():
            shutil.copytree(src, backup_location, dirs_exist_ok=True)
        else:
            shutil.copy2(src, backup_location)
        return True
    return False
