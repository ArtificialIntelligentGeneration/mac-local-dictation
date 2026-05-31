# Agent Rules (DictationApp)

**CRITICAL: NEVER MODIFY OR REWRITE THE `DictationApp.py` FILE UNDER ANY CIRCUMSTANCES.**

## 1. Do Not Edit the Code
This is a local Whisper-based dictation application. It is extremely fragile regarding macOS system permissions (Accessibility). Any modification to `DictationApp.py` breaks the application's signature, causing macOS to silently revoke keystroke emulation permissions (the app will recognize voice but fail to type text).
**If the user asks you to start, fix, or install the dictation app, DO NOT attempt to refactor the code.**

## 2. Launching the App
- Always run **THIS exact stable version** from the current directory.
- Do not create duplicates. Always kill the old process before starting a new one:
  `pkill -f DictationApp.py`
- Run the application in the background so it doesn't block the terminal (use `is_background: true` in `run_shell_command`, or `nohup`).

## 3. Troubleshooting
- **If text is not being typed:** Tell the user to go to **System Settings -> Privacy & Security -> Accessibility**, remove their terminal/Python from the list (using the `-` button), and add it back (using the `+` button). This is required due to macOS security policies for scripts emulating keystrokes.
- **If the Swift helper is missing:** Run the `./build_and_install.sh` script. It will compile `paste_helper.swift` and place it in `/tmp/paste_helper_type`.

## 4. Maintenance
Do not touch the MLX logic (specifically the `mlx.core.clear_cache()` cleanup), do not change the `pynput` bindings, and do not add logging. Leave everything exactly as it is.