
from textFormatting import colors
import time

TEXT_SPEED = 0.0003

def lbl(text, color, interval, format):
  if format == "":
    if color == "clear":
      for letter in text:
        print(letter, end="", flush=True)
        time.sleep(interval)
    else:
      for letter in text:
        print(f"{colors[color]}{letter}{colors['reset']}", end="", flush=True)
        time.sleep(interval)
  else:
    if color == "clear":
      for letter in text:
        print(letter, end="", flush=True)
        time.sleep(interval)
    else:
      for letter in text:
        print(f"{format[format]}{colors[color]}{letter}{colors['reset']}{format['reset']}", end="", flush=True)
        time.sleep(interval)
