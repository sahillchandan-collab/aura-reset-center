# Breathe Out the Habit

Free PDF lead magnet: a guided meditation to quit smoking, plus a 15-day tracker.

## Edit and rebuild

1. Open `build_guide.py` and change the values under **EDIT THESE** (`AUTHOR`, `HANDLE`, `DAYS_FREE`).
2. Install the one dependency and build:

```bash
pip install reportlab
python3 build_guide.py
```

The output is `Breathe-Out-The-Habit.pdf` in this folder.
