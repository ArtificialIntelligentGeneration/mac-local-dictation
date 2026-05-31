import time
import subprocess
import threading
import os
import sys
import warnings

warnings.filterwarnings('ignore')

import pyperclip
import rumps
from pynput import keyboard
import mlx_whisper
import mlx.core as mx

class DictationApp(rumps.App):
    def __init__(self):
        super(DictationApp, self).__init__("⚪️", quit_button="Выход")
        self.is_recording = False
        self.mode = "IDLE"
        self.audio_file = "/tmp/hs_dictation.wav"
        self.rec_process = None
        self.recording_start_time = 0
        self.active_keys = set()
        self.d_key_active = False
        self.transcribe_lock = threading.Lock()

        self.menu = [
            rumps.MenuItem("Очистить буфер", callback=self.clear_buffer)
        ]

        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.listener.start()

    def clear_buffer(self, _):
        pyperclip.copy("")
        rumps.notification("Dictation", "", "Буфер очищен")

    def set_status(self, status):
        if status == "RECORDING":
            self.title = "🔴"
        elif status == "TRANSCRIBING":
            self.title = "🟡"
        else:
            self.title = "⚪️"

    def paste_text(self, text):
        if not text:
            return
            
        pyperclip.copy(text)
        
        # Hard wait to ensure the user physically released Cmd+D
        time.sleep(0.4)
        
        try:
            # We call the new Swift binary that uses direct unicode typing
            subprocess.run(['/tmp/paste_helper_type', text])
            rumps.notification("Dictation", "Успешно", f"{text[:30]}...")
        except Exception as e:
            print(f"Paste Error: {e}")
            
        self.set_status("IDLE")

    def transcribe_and_paste(self):
        self.set_status("TRANSCRIBING")
        try:
            with self.transcribe_lock:
                result = mlx_whisper.transcribe(
                    self.audio_file,
                    path_or_hf_repo="mlx-community/whisper-large-v3-mlx"
                )
                mx.clear_cache()
            text = result.get('text', '').strip()
            self.paste_text(text)
        except Exception as e:
            print(f"Error: {e}")
            self.set_status("IDLE")

    def start_recording(self):
        self.is_recording = True
        self.mode = "EVALUATING"
        self.recording_start_time = time.time()
        self.set_status("RECORDING")
        subprocess.Popen(['afplay', '-v', '0.2', '/System/Library/Sounds/Glass.aiff'])
        self.rec_process = subprocess.Popen(['rec', '-q', '-c', '1', '-r', '16000', self.audio_file])

    def stop_and_transcribe(self):
        self.is_recording = False
        self.mode = "IDLE"
        if self.rec_process:
            self.rec_process.terminate()
            self.rec_process.wait()
        subprocess.Popen(['afplay', '-v', '0.2', '/System/Library/Sounds/Pop.aiff'])
        threading.Thread(target=self.transcribe_and_paste).start()

    def on_press(self, key):
        self.active_keys.add(key)
        has_cmd = any(k in self.active_keys for k in [keyboard.Key.cmd, keyboard.Key.cmd_l, keyboard.Key.cmd_r])
        is_d = getattr(key, 'char', None) == 'd'

        if is_d:
            if self.d_key_active:
                return
            self.d_key_active = True
            
            if has_cmd:
                if not self.is_recording:
                    self.start_recording()
                elif self.mode == "TOGGLE":
                    self.stop_and_transcribe()
                    self.d_key_active = False

    def on_release(self, key):
        try:
            self.active_keys.remove(key)
        except KeyError:
            pass
            
        is_d = getattr(key, 'char', None) == 'd'
        if is_d:
            self.d_key_active = False
            
        has_cmd = any(k in self.active_keys for k in [keyboard.Key.cmd, keyboard.Key.cmd_l, keyboard.Key.cmd_r])
        
        if self.is_recording and self.mode == "EVALUATING":
            if not (has_cmd and self.d_key_active):
                elapsed = time.time() - self.recording_start_time
                if elapsed >= 2.0:
                    self.stop_and_transcribe()
                else:
                    self.mode = "TOGGLE"

if __name__ == "__main__":
    app = DictationApp()
    app.run()
