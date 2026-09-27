# Collect Macro

Small Windows app that loops a grind routine for [Collect 1 Million Items](https://www.roblox.com/games/133363783004873/Collect-1-Million-Items) on Roblox.

You pick **Conveyor** or **Magnet**, set how long each run lasts, hit **Start**, and it handles launch → join → equip tool → wait → leave → rejoin until you stop it. Everything is keyboard/mouse automation on your desktop — no injectors, no memory hacks, no modified Roblox client.

Built for myself-style “set it and watch the log” use. YMMV on slower PCs or if Roblox moves menu items around.

## Screenshots

_Add a screenshot of the Home tab here once you have a build — helps people know what they’re downloading._

## Download the `.exe`

**Easiest:** use GitHub Actions (no Python needed on your PC).

1. Go to **Actions** → **Build Windows EXE**.
2. Click **Run workflow** → run it on `main`.
3. When the job finishes, open the run and download the **`CollectMacro-windows`** artifact (zip with `dist/` inside).

**Or build locally on Windows:**

```powershell
git clone https://github.com/YOUR_USER/collect-macro.git
cd collect-macro
.\build.ps1
```

Your exe lands in `dist\`. You can copy `CollectMacro.exe` anywhere; settings go in `config.json` next to the exe or in `%APPDATA%\CollectMacro\config.json`.

> Builds have to run on **Windows**. PyInstaller doesn’t cross-compile from Mac/Linux.

## Quick start

1. Install Roblox if you haven’t already.
2. Open **Settings** → point **Roblox executable** at `RobloxPlayerBeta.exe` (Browse button).
3. Choose **Conveyor** (default ~32s) or **Magnet** (~17s). Change durations if you want.
4. Set **grind tool key** (default `1`) and bump **join delay** if the game loads slowly.
5. **Home** → **Start**. **Stop** or **F9** (emergency stop) kills the loop immediately.

If leaving the game acts weird, tweak the **Leave** delays in Settings. The app uses **Esc → Down → Enter** like you would from the keyboard — same fragility as doing it by hand.

## What it actually does each cycle

1. Starts Roblox if it’s not open (optional).
2. Joins place ID `133363783004873`.
3. Waits your join delay, focuses the Roblox window.
4. Presses your tool hotkey.
5. Waits for Conveyor/Magnet duration.
6. Leaves the experience (menu keys).
7. Waits, rejoins, repeats — until you stop.

It won’t spawn a second Roblox if one is already running.

## Development

Python 3.11+, mainly tested as a packaged exe on Windows. UI work can happen on Mac; the macro itself needs Windows (`pywin32`, window focus, etc.).

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -r requirements.txt
pip install -e .
collect-macro
```

From a checkout without install:

```bash
set PYTHONPATH=src
python -m collect_macro
```

## Disclaimer

This is **not** official Roblox software. Automating gameplay might break Roblox’s Terms of Use or game rules — that’s on you. Authors aren’t responsible if your account gets warned or banned. Use a throwaway or accept the risk.

## License

MIT — see [LICENSE](LICENSE).
