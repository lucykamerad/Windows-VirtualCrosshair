import json
import os

# Stored next to the program so the config is found regardless of the
# directory the app is launched from.
CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "crosshair_config.json")

SHAPES = ("Cross", "Dot", "Cross + Dot", "Circle")
# (min, max) ranges matching the sliders in the settings window
LIMITS = {"size": (1, 100), "thickness": (1, 20), "opacity": (10, 255)}

DEFAULT_CONFIG = {
    "shape": "Cross",
    "color": "#00FF00", # Green
    "size": 20,
    "thickness": 2,
    "opacity": 255
}

def _sanitize(config):
    """Replace missing or invalid values (e.g. from a hand-edited file) with defaults."""
    clean = DEFAULT_CONFIG.copy()
    if not isinstance(config, dict):
        return clean
    if config.get("shape") in SHAPES:
        clean["shape"] = config["shape"]
    color = config.get("color")
    if isinstance(color, str) and len(color) == 7 and color.startswith("#"):
        try:
            int(color[1:], 16)
            clean["color"] = color
        except ValueError:
            pass
    for key, (low, high) in LIMITS.items():
        value = config.get(key)
        if isinstance(value, int) and not isinstance(value, bool):
            clean[key] = max(low, min(high, value))
    return clean


def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                # Also fills in any keys missing after an update
                return _sanitize(json.load(f))
        except Exception as e:
            print(f"Error loading config: {e}")
            return DEFAULT_CONFIG.copy()
    else:
        return DEFAULT_CONFIG.copy()

def save_config(config):
    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f, indent=4)
    except Exception as e:
        print(f"Error saving config: {e}")
