import logging
import pathlib as Path

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

# set log path to parent directory
log_path = str(Path.Path(__file__).resolve().parent) + "/EmotionEngine.log"
print(log_path)
logging.basicConfig(filename=log_path, level=log_lvl, format='%(asctime)s %(levelname)s %(threadName)-10s %(module)s %(message)s')

import threading
from displayEngine import get_device
import Emotions.blinking.blink as blink
import Emotions.starEyes.starEyes as starEyes
from Emotions.lookLeft.lookLeft import lookLeft_hold
from Emotions.lookRight.lookRight import lookRight_hold
from Emotions.shy.shy import shy_hold
from Emotions.anger.anger import anger_hold
import Emotions.utilFunctions.displayFunctions as displayFunctions
from random import randint
import time


class ThreadWithStop(threading.Thread):
    def __init__(self, *args, **kwargs):
        super(ThreadWithStop, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()
        self._lock = threading.Lock()

    def stop(self):
        logging.debug("stop %s", self._lock.locked())
        while self._lock.locked():
            logging.debug("wait for lock to be released")
            time.sleep(0.001)  # Wait a bit for the lock to be released
        self._stop_event.set()

    def stopped(self):
        logging.debug("check stopped %s", self._stop_event.is_set())
        return self._stop_event.is_set()
    
    def lock(self):
        logging.debug("lock")
        self._lock.acquire()

    def unlock(self):
        logging.debug("unlock")
        if self._lock.locked():
            self._lock.release()

    def run(self):
        while not self.stopped():
            try:
                blink.eyeOpen(display,randint(4,7))
                if self.stopped():
                    return
                self.lock()
                blink.triggerBlink(display)
            finally:
                self.unlock()


def menu():
    print("1. Blink")
    print("2. StarEyes")
    print("3. lookLeft")
    print("4. lookRight")
    print("5.shy")
    print("6. anger")
    print("99. Exit")
    choice = input("Enter your choice: ")
    logging.debug("choice: %s", choice)
    return choice

if __name__ == "__main__":
    try:
        device = get_device()
        display = displayFunctions.DisplayFunctions(device)
        blink_thread = ThreadWithStop()

        blink_thread.start()

        while True:
            logging.debug("running main thread")
            choice = menu()

            if choice == "1":
                logging.debug("Blink")
                if not blink_thread.is_alive():
                    blink_thread = ThreadWithStop()
                    blink_thread.start()

            elif choice == "2":
                logging.debug("StarEyes")
                if blink_thread.is_alive():
                    logging.debug("stop blink")
                    blink_thread.stop()
                starEyes.main(display)
                blink_thread = ThreadWithStop()
                blink_thread.start()

            elif choice == "3":
                logging.debug("lookLeft")
                if blink_thread.is_alive():
                    logging.debug("stop blink")
                    blink_thread.stop()
                lookLeft_hold(display,3)
                blink_thread = ThreadWithStop()
                blink_thread.start()

            elif choice == "4":
                logging.debug("lookRight")
                if blink_thread.is_alive():
                    logging.debug("stop blink")
                    blink_thread.stop()
                lookRight_hold(display,3)
                blink_thread = ThreadWithStop()
                blink_thread.start()

            elif choice == "5":
                logging.debug("shy")
                if blink_thread.is_alive():
                    logging.debug("stop blink")
                    blink_thread.stop()
                shy_hold(display,6)
                blink_thread = ThreadWithStop()
                blink_thread.start()

            elif choice == "6":
                logging.debug("anger")
                if blink_thread.is_alive():
                    logging.debug("stop blink")
                    blink_thread.stop()
                anger_hold(display,6)
                blink_thread = ThreadWithStop()
                blink_thread.start()


            elif choice == "99":
                logging.debug("Exit")
                blink_thread.stop()
                break            

            logging.debug("end of main thread")
    except KeyboardInterrupt:
        blink_thread.stop()