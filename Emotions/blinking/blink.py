from os import path
from pathlib import Path
from time import sleep
from random import randint

def assets_dir():
    return str(Path(__file__).resolve().parent) + "/assets"

def eyeOpen_path():
    return str(Path(__file__).resolve().parent) + "/assets/01.png"

def main(display):
    while True:
        path=assets_dir()
        display.pngs_display(path)
        display.png_display(eyeOpen_path())
        ranin = randint(4,10)
        print(ranin)
        sleep(ranin)

def eyeOpen(display,for_how_long=1):
    display.png_display(eyeOpen_path())
    sleep(for_how_long)

def triggerBlink(display):
    path=assets_dir()
    display.pngs_display(path)