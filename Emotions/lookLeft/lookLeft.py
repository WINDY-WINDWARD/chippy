import logging
from pathlib import Path

# load log level from logger.json
import json
log_lvl=""
with open('logger.json') as json_file:
    data = json.load(json_file)
    log_lvl = data['logLevel']
    if log_lvl == "info":
        log_lvl = logging.INFO
    elif log_lvl == "debug":
        log_lvl = logging.DEBUG
    elif log_lvl == "warning":
        log_lvl = logging.WARNING
    elif log_lvl == "error":
        log_lvl = logging.ERROR
    elif log_lvl == "critical":
        log_lvl = logging.CRITICAL
    else:
        log_lvl = logging.CRITICAL

log_path = str(Path(__file__).resolve().parent.parent.parent) + "/EmotionEngine.log"
print(log_path)
logging.basicConfig(level=log_lvl, filename=log_path, format='%(asctime)s %(levelname)s %(threadName)-10s %(module)s %(message)s')

import time
import os
import re


def lookLeft_hold(display,for_how_long=1):
    """Look left and hold for the given time"""
    path=str(Path(__file__).resolve().parent) + "/assets"
    logging.debug("main")
    logging.debug("display all png")
    display.pngs_display_rev(path,0)
    imageFiles = sorted([os.path.join(path, file) for file in os.listdir(path) if re.match(r'.*\.png', file)])
    # display only the last image
    logging.debug("display only the last image")
    holdLeft(display,imageFiles[-1],for_how_long)

def holdLeft(display,img_file,for_how_long=1):
    """display only the given image for the given time
        recall this function to hold the image for longer"""
    display.png_display(img_file)
    time.sleep(for_how_long)
    