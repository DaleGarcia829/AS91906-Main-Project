import json
from os.path import exists

DEFAULTS = {
    "brightness": 100,
    "audio": 70
}

MIN_BRIGHTNESS = 1
MAX_BRIGHTNESS = 100
MIN_AUDIO = 0
MAX_AUDIO = 100

class Settings:
    def __init__(self, filename):
        self._filename = filename
        self._settings = DEFAULTS.copy()
        self.load_settings()
    
    def load_settings(self):
        if exists(self._filename):
            try:
                with open(self._filename, "r", encoding="utf-8") as f:
                    self._settings = json.load(f)
            except Exception as e:
                print("Failed to read file, using defaults.", e)

    def write_settings(self):
        try:
            with open(self._filename, "w", encoding="utf-8") as f:
                json.dump(self._settings, f, indent=4)
        except Exception as e:
            print("Failed to open file for writing.", e)

    def get_brightness(self):
        return self._settings.get("brightness", 100)
        
    def set_brightness(self, brightness):
        if brightness < MIN_BRIGHTNESS:
            self._settings["brightness"] = MIN_BRIGHTNESS
        elif brightness > MAX_BRIGHTNESS:
            self._settings["brightness"] = MAX_BRIGHTNESS
        else:
            self._settings["brightness"] = brightness

    def get_audio(self):
        return self._settings.get("audio", 70)
        
    def set_audio(self, audio):
        if audio < MIN_AUDIO:
            self._settings["audio"] = MIN_AUDIO
        elif audio > MAX_AUDIO:
            self._settings["audio"] = MAX_AUDIO
        else:
            self._settings["audio"] = audio

    brightness = property(get_brightness, set_brightness, None)
    audio = property(get_audio, set_audio, None)
