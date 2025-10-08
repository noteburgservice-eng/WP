# WP

## Packaging into a standalone Windows executable

1. Ensure Python 3.11+ and pip are installed on the build machine.
2. Install PyInstaller: `pip install pyinstaller`.
3. From this directory run `pyinstaller --clean --noconsole --onefile --name SetRandomWallpaper set_random_wallpaper.py`.

The resulting executable (`dist/SetRandomWallpaper.exe`) can be copied next to the
`WP` folder on the target Windows machine. Because the Python interpreter is
embedded by PyInstaller, the executable works without requiring Python to be
installed on the device. Each launch copies a random file from the neighbouring
`WP` directory into the user's Documents folder and applies it as the desktop
wallpaper.