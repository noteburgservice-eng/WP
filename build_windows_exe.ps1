param(
    [string]$OutputName = "SetRandomWallpaper"
)

pyinstaller --clean --noconsole --onefile --name $OutputName set_random_wallpaper.py
