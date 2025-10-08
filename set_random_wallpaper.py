#!/usr/bin/env python3
"""Set the desktop wallpaper from a random file in the sibling ``WP`` directory.

The script copies the randomly chosen file into the user's Documents folder before
applying it as the desktop background. On Windows the wallpaper is applied via the
``SystemParametersInfoW`` Win32 API. On GNOME-based systems ``gsettings`` is used.

When packaged with PyInstaller the executable can be distributed without requiring a
Python installation on the target machine.
"""

from __future__ import annotations

import ctypes
import random
import shutil
import subprocess
import sys
from pathlib import Path

SPI_SETDESKWALLPAPER = 20
SPIF_UPDATEINIFILE = 0x01
SPIF_SENDWININICHANGE = 0x02


def resolve_base_dir() -> Path:
    """Return the directory containing the script or frozen executable."""

    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent


def choose_random_file(folder: Path) -> Path:
    files = [path for path in folder.iterdir() if path.is_file()]
    if not files:
        raise FileNotFoundError(
            f"No files found in '{folder}'. Add at least one file to continue."
        )
    return random.choice(files)


def copy_to_documents(source: Path) -> Path:
    documents_dir = Path.home() / "Documents"
    documents_dir.mkdir(parents=True, exist_ok=True)

    destination = documents_dir / source.name
    shutil.copy2(source, destination)
    return destination


def set_wallpaper_windows(image_path: Path) -> None:
    result = ctypes.windll.user32.SystemParametersInfoW(  # type: ignore[attr-defined]
        SPI_SETDESKWALLPAPER,
        0,
        str(image_path),
        SPIF_UPDATEINIFILE | SPIF_SENDWININICHANGE,
    )
    if result == 0:
        raise RuntimeError("Failed to set wallpaper using the Win32 API.")


def set_wallpaper_gnome(image_path: Path) -> None:
    wallpaper_uri = image_path.as_uri()
    for schema_key in ("picture-uri", "picture-uri-dark"):
        try:
            subprocess.run(
                [
                    "gsettings",
                    "set",
                    "org.gnome.desktop.background",
                    schema_key,
                    wallpaper_uri,
                ],
                check=True,
            )
        except (FileNotFoundError, subprocess.CalledProcessError) as exc:
            raise RuntimeError(
                "Failed to set wallpaper using gsettings. "
                "Ensure GNOME is installed and accessible."
            ) from exc


def set_wallpaper(image_path: Path) -> None:
    if sys.platform.startswith("win"):
        set_wallpaper_windows(image_path)
    else:
        set_wallpaper_gnome(image_path)


def main() -> None:
    base_dir = resolve_base_dir()
    source_dir = base_dir / "WP"
    if not source_dir.is_dir():
        raise FileNotFoundError(f"Folder '{source_dir}' was not found")

    chosen_file = choose_random_file(source_dir)
    destination = copy_to_documents(chosen_file)

    set_wallpaper(destination)
    print(f"Wallpaper set to {destination}")


if __name__ == "__main__":
    main()
