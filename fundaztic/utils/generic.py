import time
from pathlib import Path


def save_file(file_path: str, write_content, write_method: str = "wb") -> None:
    with open(file_path, write_method) as f:
        f.write(write_content)


def wait_and_rename_latest_download(
    download_dir: Path, new_filename: str, timeout: int = 30
):
    """
    Waits for the latest file to be downloaded into `download_dir`
    and renames it to `new_filename`.
    """
    end_time = time.time() + timeout
    while time.time() < end_time:
        files = list(download_dir.glob("*"))
        files = [f for f in files if not f.name.endswith(".crdownload")]
        if files:
            latest_file = max(files, key=lambda f: f.stat().st_mtime)
            new_path = download_dir / new_filename
            if new_path.exists():
                new_path.unlink()  # Delete existing file before rename
            latest_file.rename(new_path)
            return
        time.sleep(1)
    raise TimeoutError("Download did not complete in time.")


def delete_file():
    for path in ["files", "images"]:
        p = Path(path)
        for file in p.iterdir():
            if file.is_file():
                file.unlink()  # delete the file
