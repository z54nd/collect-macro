# Build CollectMacro.exe with PyInstaller (run on Windows).
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root

if (-not (Test-Path ".venv")) {
    python -m venv .venv
}
& .\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt

$Hidden = @(
    "customtkinter",
    "pynput",
    "pynput.keyboard",
    "pynput.keyboard._win32",
    "pynput.mouse",
    "pynput.mouse._win32",
    "pyautogui",
    "psutil",
    "win32timezone"
)

$HiArgs = foreach ($h in $Hidden) { "--hidden-import"; $h }

pyinstaller @(
    "--noconfirm",
    "--clean",
    "--windowed",
    "--name", "CollectMacro",
    "--paths", "$Root\src"
) + $HiArgs + @(
    "$Root\src\collect_macro\__main__.py"
)

Write-Host ""
Write-Host "Build complete. See dist\CollectMacro\ or dist\CollectMacro.exe"
Write-Host "Config: config.json beside exe, or %APPDATA%\CollectMacro\config.json"
