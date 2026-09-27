# Collect Macro

Collect Macro is a Windows application made for automating a simple grind routine in [Collect 1 Million Items](https://www.roblox.com/games/133363783004873/Collect-1-Million-Items) on Roblox.

The application handles the repetitive parts of the routine for you, including joining the game, selecting your grind tool, waiting for the configured amount of time, leaving the game, and repeating the process.

## Download

You do **not** need Python, Git, Roblox Studio, or any development tools to use Collect Macro.

### Download the `.exe`

1. Open the **Releases** section on the right side of this GitHub page.
2. Open the **latest release**.
3. Scroll down to the **Assets** section.
4. Find **`CollectMacro.exe`**.
5. Click **`CollectMacro.exe`** to download it.
6. Once the download is finished, open the file.
7. If Windows shows a security warning, select **More info** and then **Run anyway** if you trust the file.

The `.exe` is the complete application. You do not need to install Python or download any additional files.

## How to use

Once Collect Macro is open:

1. Make sure Roblox is installed and working normally.
2. Open the **Settings** tab.
3. Select your Roblox executable if required.
4. Choose your grind tool:

   * **Conveyor**
   * **Magnet**
5. Set the amount of time you want the macro to stay in the game.
6. Check the other settings and adjust them if necessary.
7. Go back to the **Home** tab.
8. Press **Start**.
9. Collect Macro will handle the routine automatically.

You can stop the macro at any time using the **Stop** button or the configured emergency stop hotkey.

## What the macro does

A normal cycle works like this:

1. Starts Roblox if it is not already running.
2. Joins **Collect 1 Million Items**.
3. Waits for the game to load.
4. Focuses the Roblox window.
5. Presses the configured grind tool key.
6. Waits for the configured grind duration.
7. Leaves the Roblox experience.
8. Waits before joining again.
9. Repeats the process until you stop the macro.

The application is designed to reuse an existing Roblox process instead of intentionally opening multiple Roblox clients.

## Grind tools

Collect Macro supports two grind tools:

**Conveyor**

The default routine is approximately **32 seconds** per run.

**Magnet**

The default routine is approximately **17 seconds** per run.

The timings can be changed from the application settings if the game changes or your setup requires different timings.

## Windows security warning

Because Collect Macro is distributed as a standalone Windows executable and may not have a commercial code-signing certificate, Windows Defender or SmartScreen may display a warning when you first open it.

If you downloaded the file from the official GitHub repository and understand what you are running, Windows may allow you to continue by selecting:

**More info → Run anyway**

Only run executable files that you trust.

## Updates

When a new version is released, download the newest `CollectMacro.exe` from the latest GitHub Release.

You can simply replace your old executable with the new one.

Your settings may be stored separately depending on the version and configuration of the application, so updating the executable should not require rebuilding or installing Python.

## Troubleshooting

### Roblox does not open

Make sure Roblox is installed and that you can launch it normally before starting Collect Macro.

Check the Roblox executable path under **Settings** if the application asks you to select it.

### The macro starts too early

Increase the **join delay** in Settings.

This gives Roblox more time to load before Collect Macro starts interacting with the game.

### The wrong tool is selected

Check the configured **grind tool key** and make sure it matches the key used by the game.

The default key is `1`.

### Leaving the game does not work

The leave routine uses normal keyboard interaction with Roblox. If Roblox changes its menu layout or the timing is different on your computer, adjust the relevant leave delays in Settings.

### The macro stops unexpectedly

Check the activity log on the Home tab.

The log can show what the application was doing when the problem occurred.

## Requirements

Collect Macro is intended for **Windows**.

You need:

* Windows
* Roblox
* A working internet connection
* The downloaded `CollectMacro.exe`

You do **not** need:

* Python
* Git
* Visual Studio
* Roblox Studio
* Any additional programming software

## Disclaimer

Collect Macro is an independent third-party application and is **not affiliated with, endorsed by, or sponsored by Roblox**.

Automating gameplay may be against the rules of Roblox or the individual game. You are responsible for how you use the application and for following the applicable rules.

Use the software at your own discretion. The developer is not responsible for actions taken against your Roblox account as a result of using the application.

## License

Private License.

See [`LICENSE`](LICENSE) for the full license.
