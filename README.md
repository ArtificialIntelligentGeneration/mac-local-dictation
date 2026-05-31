# Mac Local Dictation (Free SuperWhisper Alternative)

🎁 **A Gift to the Community:** This is a completely free, open-source alternative to paid, subscription-based dictation apps (like SuperWhisper). Use it for free, forever! It excellently recognizes mixed languages (e.g., Runglish) and works entirely offline.

## 🤖 AI-Friendly (Agent-Driven Installation)
This repository is designed for "lazy" installation via AI agents (Cursor, Windsurf, Claude Code, Gemini CLI, Aider, etc.).
You don't need to understand the code or run terminal commands manually. Just clone the repo, open it in your favorite AI IDE, and give it the prompt:

> *"Install and run this dictation app."*

The project contains strict, standardized agent instructions (`.cursorrules`, `CLAUDE.md`, `AGENTS.md`, `GEMINI.md`). Your agent will read them, correctly compile the Swift helper, set up the background process, and most importantly, **will not break** the fragile macOS Accessibility permissions by trying to "improve" the code.

## Features
- **Local & Private**: No data ever goes to the cloud (Whisper runs locally on the Apple Silicon GPU).
- **Hold-to-Talk or Toggle**: Hold `Cmd + D` (or double-press), dictate your text, and release. The text is automatically typed into your active window.
- **Native Swift Injection**: The app uses native macOS `CGEvent` to emulate keystrokes, bypassing the clipboard. This allows dictation to work smoothly even in input fields where `Cmd+V` is blocked or buggy.
- **MLX Metal OOM Protection**: Includes a built-in workaround for the known `SIGABRT` bug in older MLX versions. GPU memory is forcefully cleared (`mlx.core.clear_cache()`) after every transcribed phrase to prevent crashes.

## 🏗 Architecture & Security (Audit Notes)
This app was originally built for personal use. A recent security audit highlighted the following architectural choices you should be aware of:
- **Use of `/tmp`**: The compiled Swift helper (`paste_helper_type`) and temporary audio files (`hs_dictation.wav`) are stored in the system's `/tmp` directory. This ensures maximum I/O speed, but `/tmp` is accessible to other local processes and is wiped when the Mac restarts.
- **What this means**: If you reboot your computer, you will need to restart the script (or set up a Login Item/auto-start script). If you have strict local security requirements, feel free to fork the repo and move these temporary files into a secure application sandbox.

## Requirements
- Mac with Apple Silicon (M1/M2/M3/M4, etc.)
- Python 3.9+
- Installed `ffmpeg` and `sox` (for audio recording: `brew install sox`)

## Manual Installation (Without an AI Agent)
1. Clone the repository:
   ```bash
   git clone https://github.com/ArtificialIntelligentGeneration/mac-local-dictation.git
   cd mac-local-dictation
   ```
2. Run the install script (compiles the Swift helper and installs PIP packages):
   ```bash
   ./build_and_install.sh
   ```
3. Run the app in the background:
   ```bash
   nohup python3 DictationApp.py > /dev/null 2>&1 &
   ```

## Crucial: Accessibility Permissions
For the app to intercept the global `Cmd+D` hotkey and type text autonomously, it requires macOS Accessibility permissions.
1. Go to **System Settings** -> **Privacy & Security** -> **Accessibility**.
2. Grant permission to your Terminal (or Python).
3. **WARNING:** Permissions are strictly tied to the binary's signature. If you or an AI agent modify the `DictationApp.py` file, macOS will silently revoke typing permissions. **Fix:** Remove the app from the Accessibility list (using the `-` button) and add it back (using the `+` button).